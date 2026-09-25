# Agno e Mastra: Tempo de execução da produção
# Tempo de execução do agente de produção  Instalação rápida e fluxos de trabalho tipografados

> Um agente de produção otimiza o tempo de execução do que os frameworks de prototyping ignoram: custo de instanciamento, superfícies de fluxo de trabalho digitalizadas e um backend pronto para servido. O acoplamento de 2026: Agno (Python) visa instanciamento de agente de microsecondas e backends FastAPI sem estado. Mastra envia agentes, ferramentas, fluxos de trabalho, roteamento de modelo unificado e armazenamento composto no substrato Vercel AI SDK.

**Type:** Learn | **类型:** 学习
**Languages:** Python, TypeScript | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 01 (Agent Loop), Phase 14 · 13 (LangGraph) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Identificar os objetivos de desempenho do Agno e quando são importantes.
- Nomear os três primitivos de Mastra  Agentes, Ferramentas, Fluxos de Trabalho  e os adaptadores de servidor suportados.
- Explique por que um backend FastAPI sem estatuto é o caminho recomendado para a produção Agno.
- Escolha Agno vs Mastra para uma determinada pilha (Python-primeiro vs TypeScript-primeiro).

## O problema é o problema da introdução

LangGraph, AutoGen, CrewAI são pesados em estrutura. As equipes que querem "apenas o loop do agente, rápido, no meu tempo de execução" alcançam Agno (Python) ou Mastra (TypeScript). Ambos trocam alguns dos primitivos de propriedade do framework por velocidade bruta e um ajuste mais próximo à pilha circundante.

> LangGraph、AutoGen、CrewAI são um quadro de trabalho muito pesado. Querendo "só se o Agente ciclo, rápido, em meu tempo de funcionamento" a equipe escolhe Agno (Python) ou Mastra (TypeScript) ⋅ ambos abandonaram algumas das linguagens originais do quadro, em troca de velocidade original e uma adaptação mais próxima à tecnologia ao redor.


> **【中文解读】**Agno 和 Mastra  representa as duas espécies de Agente de 2026 运行时设计哲学。Agno(原 PhiData) busca极简以最小代码构建 Agent。Mastra(TypeScript) busca plenos recursos fornecer um Agente completo 生命周期管理。

> **{【拓展：Agno (GitHub 15k+ stars) 和 Mastra 是 2026 年 Agent 运...】}**Agno (GitHub 15k+ estrelas) 和 Mastra é um novo programa de 2026 ano de Agente 运行时的新秀。Agno filosofia é 'Agent 即函数' Cada Agente é uma função diferente com um conjunto de ferramentas‛Mastra 基于TypeScript,面向全开发者,提供完整的Agente 生命周期管理(部署、监控、扩展)。 ambos suportam vários modelos 后端和 MCP 集成──

> - Não .**【前置】**必須先掌握:Fase 14·01(Agent Loop) e Fase 14·13(LangGraph) 本节是这两者"轻量替代品"──如果您不知道为什么要"轻量化"LangGraph,说明您还没在生产中遇到LangGraph的工程负担,建议先使用LangGraph 几周再回头看本节──

## O conceito central.

### Agno

- Tempo de execução do Python, anteriormente Phi-data.
- "Não há gráficos, cadeias ou padrões complicados, apenas Python puro".
- Objectivos de desempenho de seus documentos: ~ 2μs instantiation agente, ~ 3,75 KiB de memória por agente, ~ 23 fornecedores de modelos.
- Percurso de produção: backend FastAPI sem estado de sessão. Cada solicitação inicia um novo agente; estado de sessão vive em um DB.
- Multimodal nativo (texto, imagem, áudio, vídeo, arquivo) e RAG agente.

Os objetivos de velocidade importam quando você tem milhares de agentes de curta duração por segundo (fantasma de bate-papo, pipelines de avaliação), mas não importam quando um agente corre por 10 minutos.

> - Não .**【类比】**Agno 像摩托车、LangGraph 像 SUV:摩托车启动快、轻便、能钻小(2μs 实例化、3.75 KiB 内存),适合短途高频通勤(每秒数千短任务);SUV 装得多、能跑长途、有空调导航(持久化、人回路、复杂图), mas iniciação、慢占地大──**关键洞察**Não é porque é melhor, mas porque o seu cenário é "altos e curtos"

> A velocidade do objetivo é importante quando tens milhares de agentes de curta duração por segundo. Quando um agente funciona por 10 minutos, não são tão importantes.

> Agno 和 Mastra é um agente de classe leve. Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos fornecem um agente de menor quantidade.

### Mastra

- TypeScript, construído no SDK Vercel AI.
- Três primitivos:**Agents**- Não .**Tools**(Típico de zona), **Workflows**- Não .
- Roteador Modelo Unificado  3.300+ modelos em 94 provedores (março 2026).
- Armazenamento composto: memória, fluxos de trabalho, observabilidade para diferentes backends; ClickHouse recomendado para observabilidade em escala.
- Apache 2.0 com `ee/`Directórios sob licença empresarial disponível na fonte.
- Adaptadores de servidor para Express, Hono, Fastify, Koa; integração Next.js e Astro de primeira classe.
- Navio Mastra Studio (host local:4111) para depuração.
- 22k+ estrelas do GitHub, 300k+ downloads semanais em 1.0 (Jan 2026).

### Posicionamento

Nem sequer tentam ser LangGraph.

>  ambas não estão tentando se tornarem LangGraph                                                                                                                                                                                                                                                        

> Agno 和 Mastra é um agente de classe leve. Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos fornecem um agente de menor quantidade.

- **Language fit.**Agno para as equipes Python-primeira; Mastra para TypeScript-primeira.
- **Runtime ergonomics.**Agno = quase zero despesas gerais; Mastra = integrado com o ecossistema Vercel.
- **Observability.**Ambos se integram com Langfuse/Phoenix/Opik (Lessão 24) mas o Mastra Studio é de primeira parte.

### Quando escolher cada um

- **Agno**Python backend, muitos agentes de curta duração, fortes requisitos de perf, FastAPI loja.
- **Mastra** Backend TypeScript, Next.js / Vercel deployment, roteamento unificado de modelos multi-provedor, ferramentas Zod-typed.
- **LangGraph**(Lessão 13)  quando o estado durável e o raciocínio gráfico explícito importam mais do que a velocidade bruta.
- **OpenAI / Claude Agent SDK** quando se quer a forma produtizada do fornecedor (Lessões 1617).

### Onde este padrão vai mal

> ️ **【易错点】**看到Agno "2μs 实例化"就无脑选Agno。**后果**Se o seu cenário for "uma solicitação de executar um Agente de 10 minutos", 2μs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      **一行修复**A primeira medida é a de "Agente  casos de expansão × casos de expansão em relação ao total de expansão", que representa > 30% da capacidade de desempenho.

- **Perf-for-perf's-sake.**A escolha do Agno porque "2μs" soa bem quando a carga de trabalho é uma chamada lenta por pedido.
- **Ecosystem lock-in.**A integração com sabor a Vercel de Mastra é um mais em Vercel, um menos em outros lugares.
- **Enterprise license confusion.**O Mastra `ee/`Os diretórios estão disponíveis em fonte, não no Apache 2.0.

> 🤔 **【困惑】**P: Meu grupo é Python 后端, quer mais a função "多模型路由" de Mastra, pode usar Agno 实现? A: 能, mas para escrever por si mesmo. Agno também tem ~23 fornecedores de modelos, mas o fornecedor de Mastra 3300 + modelo 94 é baseado no enorme ecossistema do Vercel AI SDK. Se o "model路由" é o principal recurso e o grupo aceita TypeScript, Mastra é a escolha mais provável; se se perseverar em Python, Agno + auto-embolso um modelo de roteador de camada também vai, o volume de trabalho é de cerca de 2-3 天── não é um quadro de decisão da tecnologia, reversão.

> **为性能而性能。**Porque os 2μs parecem não ser errados em escolher Agno, e o trabalho é cada pedido de um Agente Rápido.
> **生态系统锁定。**Mastra's Vercel 风格集集集在Vercel 上是优势,在其他地方是劣势.
> **企业许可困惑。**Mastra de `ee/`O código-fonte é disponível, não é Apache 2.0. Se você está planejando forque, leia a licença.

## Construí-lo e realizei-o.
```figure
wb-runtime-spawn
```

## Construí-lo

Esta lição é principalmente comparativa  nenhum artefato de código único faria justiça para ambos os quadros. Veja `code/main.py`Para um brinquedo lado a lado: um mínimo de "exercer um agente, fluir a saída, persistir sessão" fluxo implementado duas vezes (uma vez em forma de Agno, uma vez em forma de Mastra).

> Esta aula é principalmente comparativa. Não há um produto de código capaz de simultaneamente expressar as características de dois quadros.`code/main.py`O processo de "agência de operação" é realizado duas vezes (uma Agno 形态, outra Mastra 形态).

> Agno 和 Mastra é um agente de classe leve. Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos fornecem um agente de menor quantidade.

- É o que é ?

```
python3 code/main.py
```

Duas traças estruturalmente diferentes, mas funcionalmente equivalentes.

>                                                                                                                                                                                                                                                               

> Agno 和 Mastra é um agente de classe leve. Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos fornecem um agente de menor quantidade.

## Use-o com o framework implementado.

- **Agno** Python backend que precisa de velocidade e forma FastAPI.
- **Mastra** Backend do TypeScript com muitos provedores e primitivos de fluxo de trabalho.
- Ambos os ganchos de observação de primeira parte da nave, ambos integrados com o Langfuse.

## Envia-o . Produto .

`outputs/skill-runtime-picker.md`escolhe Agno, Mastra, LangGraph ou um SDK do provedor com base na pilha, no orçamento de latência e na forma operacional.

> `outputs/skill-runtime-picker.md`根据技术、延迟预算和运营形态选择 Agno、Mastra、LangGraph 或供应商 SDK──

> Agno 和 Mastra é um agente de classe leve. Agno 专注快速构建,Mastra 专注 TypeScript 生产部署── ambos fornecem um agente de menor quantidade.

## Exercícios.

1. Leia os documentos do Agno, transporte o loop do STDlib ReAct para Agno.
  Tradução do inglês para tradução do inglês:
2. Leia os documentos de Mastra. Portar o mesmo ciclo para Mastra. O que mudou na digitação de ferramentas (Zod vs nada)?
  Tradução do inglês para tradução do inglês:
3. Método de referência: medir a latência de instanciamento do agente na sua pilha.
  Tradução do inglês para tradução do inglês:
4. Desenhar uma migração: se você está executando CrewAI em Python, o que se rompe se você se mudar para Agno?
  Tradução do inglês para tradução do inglês:
5. Leia o Mastra `ee/`Que restrições afetariam um fork de código aberto?
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Agno | "Fast Python agents" | Stateless session-scoped agent runtime |  |
| Mastra | "TypeScript agents on Vercel AI SDK" | Agents + Tools + Workflows + Model Router |  |
| Unified Model Router | "Multi-provider access" | Single client for 3,300+ models across 94 providers |  |
| Composite storage | "Multiple backends" | Memory/workflows/observability each to a different store |  |
| Mastra Studio | "Local debugger" | localhost:4111 UI for introspecting agents |  |
| Source-available | "Not OSS" | License permits source reading but restricts commercial use |  |

## Mais leitura 延伸阅读

- [Agno Agent Framework docs](https://www.agno.com/agent-framework) Objectivos de desempenho, integração da FastAPI
  Tradução do português:
- [Mastra docs](https://mastra.ai/docs) primitivos, adaptadores de servidores, Router Modelo
  Tradução do português:
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) a alternativa de grafico estadual
  Tradução do português:
- [Comet Opik](https://www.comet.com/site/products/opik/) comparações de observabilidade citadas pelas integrações de Mastra
  Tradução do português:
