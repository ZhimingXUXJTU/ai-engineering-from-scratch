# LLM Observabilidade Stack Seleção .

> O mercado de observabilidade de 2026 divide-se em duas categorias. As plataformas de desenvolvimento (LangSmith, Langfuse, Comet Opik) combinam o monitoramento com avaliações, gestão de prompt, repetições de sessões. As ferramentas de gateway/instrumentamento (Helicone, SigNoz, OpenLLMetry, Phoenix) focam-se na telemetria. Langfuse é um núcleo licenciado pelo MIT com forte balanço OSS (50K eventos / mês nuvem gratuita). Phoenix é OpenTelemetry-native sob Licença Elastica 2.0  excelente para visualização drift/RAG, não um backend de produção persistente. O Arize AX usa uma integração Iceberg/Parquet de cópia zero, afirmando que é 100 vezes mais barato do que a observabilidade monolitica. LangSmith lidera para LangChain/LangGraph, $39/usuário/mês, auto-host em Enterprise apenas. O Helicone é baseado em proxy com configuração de 15-30 minutos, 100K de req/mo livre, mas menos profundidade em vestígios de agentes. Padrão de produção comum: Gateway (Helicone/Portkey) + plataforma de avaliação (Phoenix/TruLens) colada pela OpenTelemetry.

> **【中文解读】**Esta secção apresenta o Mestrado em Direito e Tecnologia da Comunicação.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy trace-sampling simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 14 (Agent Engineering)

> - Não .**【前置】**學本节前 請先掌握:Fase 17·08(推理指标) 、Fase 14(Agenta 工程) ⋅LLM 可观测性两类工具:开发平台 + Gateway/遥测。
> - Não .**【类比】**O programa de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste de teste
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Distinguir as plataformas de desenvolvimento (agrupadas: evals + prompts + sessões) das ferramentas de gateway/telemetria (só traços + métricas).
  Tradução do inglês para tradução chinesa:区分开发平台 (Bund:评估 + 提示管理 + 会话)
- Mapear seis principais ferramentas (Langfuse, LangSmith, Phoenix, Arize AX, Helicone, Opik) para suas licenças, preços e casos de uso do sweet-spot.
  中文翻译:将将六个主要工具(Langfuse、LangSmith、Phoenix、Arize AX、Helicone、Opik)映射到其许可、定价和最佳用例──
- Explique o padrão de cola OpenTelemetry que permite combinar uma ferramenta de gateway com uma plataforma de avaliação separada.
  O modelo de OpenTelemetry permite que você consiga usar ferramentas de internet com um conjunto de plataformas de avaliação independente.
- Nomear o diferenciador de custos de 2026 (abordagem de cópia zero do Arize AX vs ingestão monolitica) e indicar o multiplicador de 100x aproximado.
  O método de produção de AX é o mesmo que o método de produção de AX (Arizé AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em inglês: AX) (em alemão: AX) (em alemão: AX) (em alemão: AX) (em alemão: AX) (em alemão: AX) (em alemão: AX) (em alemão: AX) (em alemão: AX) (em alemão: AX) (em alemão: AX) (em inglês: AX) (em alemão: AX) ().

## O problema é o problema da introdução

> **【中文解读】**LLM 可观测性工具分为两类:(1) 开发平台(LangSmith、Langfuse、Opik) 捆绑监控、评估、提示管理、会话回放;(2) 网关/遥测工具(Helicone、SigNoz、OpenLLMetry、Phoenix) 专注于遥测采集──选择涉涉及四个维度:技术(LangChain?原始SDK、?) 需求许可证(MIT only?商业可接受?)、预算、自托管──

> **【拓展：LLM 可观测性市场格局】**O programa de programação é o principal dos principais jogadores do mercado de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de programação de

Você enviou um recurso LLM. Funciona. Você não tem visibilidade em falhas rápidas, loop de ferramentas, regressões de latência, picos de custo ou taxa de sucesso de caché rápido. Você Google "observabilidade LLM" e obtém oito ferramentas todas alegando que resolvem o mesmo problema em três pontos de preço diferentes.

Eles não resolvem o mesmo problema. LangSmith responde "por que essa execução de LangGraph falhou?" Phoenix responde "meu pipeline RAG está a driftar?" Helicone responde "qual aplicativo está a queimar tokens?" Langfuse responde "eu posso auto-hostar a coisa toda?" Ferramentas diferentes, públicos diferentes.

A selecção envolve quatro eixos: pilha (LangChain? SDK bruto? multi-vendor?), tolerância à licença (apenas MIT? Elastic OK? multa comercial?), orçamento (nível gratuito? $100/mo? $1000/mo?), e auto-host (deve ser bom para ter? nunca?).

## O conceito central.

### Duas categorias

**Development platforms**O que é que você tem de fazer é fazer experiências, ver qual prompt funcionou, regressão de dados, um novo prompt contra antigos vencedores.

**Gateway/telemetry tools**Infraestrutura de inferência de chamadas  prompt, resposta, tokens, latência, modelo, custo. Helicone, SigNoz, OpenLLMetry, Phoenix. Minimalista. Pode ser combinado com uma ferramenta de avaliação separada através de OpenTelemetry.

### Balanço de Langfuse  OSS

> **【拓展：LLM 可观测性工具选型决策】**2026 ano LLM 可观测性工具选型的关键维度:(1) 技术LangChain/LangGraph 生态优先选 LangSmith;自研 SDK 选 Langfuse或Phoenix;(2) 许可证要求 MIT 选 Langfuse/Opik;Elastic License 2.0 可接受选 Phoenix;商业可选 LangSmith;(3) 接受自托管必须自托管选 Langfuse或Opik(Docker 部署);(4) 预算免费层 Langfuse 50K eventos/mês、Helicone 100K req/mês;(5) 规模>10M traces/day 选 Arize AX zero-copy 架构;;

- Core Apache / MIT licenciado; auto-host via Docker.
- Número gratuito em nuvem: 50 mil eventos por mês.
- Evals, gestão rápida, rastreamento, conjuntos de dados, cobertura razoável de todas as quatro características da plataforma de desenvolvimento.
- O ponto mais interessante: você quer recursos da classe LangSmith, mas deve ser auto-host ou ficar com a licença OSS.

### Phoenix (Arize)  Telemetria-primeira, OpenTelemetry-nativa

- Licença Elastica 2.0; auto-host trivial.
- Excelente em RAG e visualização de deriva.
- Não concebido como backend de produção persistente  observabilidade primordial no tempo de desenvolvimento.
- Ponto de interesse: desenvolvimento de tubos RAG, depuração de deriva, pares com uma porta de entrada separada para produção.

### Arize AX  a escala de jogo

- Integração de dados de zero cópia através de Iceberg/Parquet.
- A matemática: você armazena vestígios no seu próprio Parquet no S3; Arize lê diretamente.
- Ponto de espera: > 10 milhões de traços por dia, lago de dados existente, quer painéis de controle específicos para LLM sem preços Datadog.

### LangSmith  LangChain/LangGraph primeiro

- Commercial, 39 dólares por mês, auto-host só na Enterprise.
- É o melhor de classe para as pilhas LangChain e LangGraph.
- O ponto doce: equipa comprometida com a LangChain, dispostos a pagar.

### Helicone  baseado em proxy

- 15-30 minutos de configuração trocando o seu `OPENAI_API_BASE`Para o proxy do Helicone.
- Licenciado pelo MIT; 100 mil reais por mês gratuitos, pagos 20 dólares por mês.
- Inclui falhas, cache, limites de taxa  também atua como um gateway.
- Menos profundidade em agentes / traços de vários passos.
- Sweet spot: início rápido, aplicativo de pilha única, precisa de gateway + observabilidade em um.

### Opik (Comet)  Plataforma de desenvolvimento OSS

- Apache 2.0, totalmente sob controle.
- Características semelhantes ao Langfuse com patrimônio cometa.
- Equipes de ML já no Comet, querem observabilidade LLM no mesmo painel.

### SigNoz  OpenTelemetry-first APM completo

- Apache 2.0. lida com APM geral mais LLM através da OpenTelemetry.
- O ponto ideal: observabilidade unificada entre os serviços e as chamadas de LLM.

### A cola: OpenTelemetry + convenções semânticas da GenAI

> **【中文解读】**A OpenTelemetry lançou o GenAI 语义约定 em 2025.`gen_ai.system`- Não.`gen_ai.request.model`- Não.`gen_ai.usage.input_tokens`), fazer diferentes ferramentas se operarem mutuamente. O modelo de produção de 2026 é: 1) de cada LLM 调用发发带 GenAI 约定的 OTel; 2) 路由到网关; 3) 双写到评估平台; 3) 双写到评估平台; 4) 归归检测; 4) 存档到数据湖; 4) 冰berg) através de Arize AX ou DuckDB fazer análises de longo prazo.

> **【拓展：LLM 可观测性的成本控制】**Em > 1M Pequeno/semana escala, o total de traços de manutenção custo excede LLM 调用本身──采样策略:100% 错误、100% 高成本请求、5% 成功请求──始终保留聚合数据,只对长尾保留原始追踪──Langfuse 50K eventos/mês 免费层适合小团队;大规模部署建议使用OpenTelemetry Collector +自有数据湖架构,成本可降低80%+──

A OpenTelemetry publicou convenções semânticas da GenAI no final de 2025 (`gen_ai.system`- Não .`gen_ai.request.model`- Não .`gen_ai.usage.input_tokens`O modelo de produção emergente:

1. Emitir OTel com convenções da GenAI de cada chamada de LLM.
2. Rota para o portal (Helicone / Portkey) para o dia-a-dia.
3. Dual-ship-to-evaluation (Phoenix/Langfuse) para regressões.
4. Arquivo no lago de dados (Iceberg) para análise a longo prazo através do Arize AX ou DuckDB.

### A armadilha: instrumentação na camada errada

> **【中文解读】**埋点层级的选择:在 Agent 框架内埋点 (如添加 LangSmith traces) 会合到这个框架;在 HTTP/OpenAI-SDK 层埋点 (通过 OpenLLMetry或网关)则可移植──2026 最佳实践是协议层埋点无论底层使用什么框架,都通过 OpenTelemetry + GenAI 语义约定统一采集──

Instrumentar dentro de sua estrutura de agente (por exemplo, adicionando traços LangSmith) o acopla a essa estrutura. Instrumentar na camada HTTP/OpenAI-SDK (através do OpenLLMetry ou do seu gateway) é portátil.

### Amostragem  não pode ficar tudo

A retenção de dados completos custa mais que as chamadas de LLM. Amostra por regras: 100% de erros, 100% de alto custo, 5% de sucesso.

### Números que você deve lembrar

- Nuvem livre Langfuse: 50 mil eventos por mês.
- LangSmith: 39 dólares por utilizador por mês.
- Helicone livre: 100 mil reais por mês.
- Arize AX afirmação: ~ 100 vezes mais barato do que monolitico em escala.
- Convenções da OpenTelemetry GenAI: 2025 transporte marítimo, 2026 amplamente adotada.

## Use-o com o framework implementado.
```figure
i4-otel-glue
```

## Usá-lo

`code/main.py`Simula um dia de rastreamento de 1M em todas as estratégias de retenção (100% ingestão, amostragem, amostragem + erros).

> `code/main.py`Simula um dia de rastreamento de 1M em todas as estratégias de retenção (100% ingestão, amostragem, amostragem + erros).

> `code/main.py`Simula um dia de rastreamento de 1M em todas as estratégias de retenção (100% ingestão, amostragem, amostragem + erros).

## Envia-o . Produto .

Esta lição produz`outputs/skill-observability-stack.md`. Dada a pilha, a escala, o orçamento, a posição da licença, escolhe a ferramenta ((s).

> 本课产 出 `outputs/skill-observability-stack.md`. Dada a pilha, a escala, o orçamento, a posição da licença, escolhe a ferramenta ((s).

## Exercícios.

1. A sua equipa na LangChain quer a observabilidade auto-hostada do OSS.
   Tradução do inglês para o inglês: Your team uses LangChain, want to open source from托管可观测性──选择 Langfuse 或 Opik 并说明理由──
2. Com 5M traços por dia com Datadog citar $ 150K por mês, calcular o equilíbrio para Arize AX.
   Tradução do inglês: In 5M traces/day 规模下,Datadog 报价$ 150K/月,计算 Arize AX 零拷贝方案的亏平衡点──
3. Desenhar um atributo OpenTelemetry GenAI definido as diretrizes da sua organização devem ser obrigatórias em cada chamada de LLM.
   Tradução do inglês para "design a your organization" (design a sua organização)
4. Discutir se Phoenix sozinho é suficiente para a produção.
   O Phoenix 单独使用是否足足以满足生产需求──它在什么情况下不够?
5. O helicóptero tem 20 ms de carga por proxy.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| OpenLLMetry | "OTel for LLMs" | Open-source OpenTelemetry instrumentation for LLMs |
| GenAI conventions | "OTel attributes" | Standard OTel attribute names for LLM calls |
| LangSmith | "LangChain observability" | Commercial platform bundled with LangChain ecosystem |
| Langfuse | "OSS LangSmith" | MIT OSS with similar feature set |
| Phoenix | "Arize dev tool" | OpenTelemetry-native dev/eval platform |
| Arize AX | "scale observability" | Commercial zero-copy Iceberg/Parquet observability |
| Helicone | "proxy observability" | HTTP proxy collecting LLM telemetry + gateway features |
| Opik | "Comet LLM" | Apache 2.0 OSS dev platform from Comet |
| Session replay | "trace rerun" | Replay a full agent session with tool calls |
| Eval | "offline test" | Running candidate model/prompt over labeled dataset |

## Mais leitura 延伸阅读

- [SigNoz — Top LLM Observability Tools 2026](https://signoz.io/comparisons/llm-observability-tools/)
- [Langfuse — Arize AX Alternative analysis](https://langfuse.com/faq/all/best-phoenix-arize-alternatives)
- [PremAI — Setting Up Langfuse, LangSmith, Helicone, Phoenix](https://blog.premai.io/llm-observability-setting-up-langfuse-langsmith-helicone-phoenix/)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Arize Phoenix docs](https://docs.arize.com/phoenix)
- [Helicone docs](https://docs.helicone.ai/)
