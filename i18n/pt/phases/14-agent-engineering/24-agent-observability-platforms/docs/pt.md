# Agente Observação: Langfuse, Phoenix, Opik

> Três plataformas de observabilidade de agentes de código aberto dominam 2026. Langfuse (MIT)  6M+ instalações / mês, rastreamento + gerenciamento de prompt + evals + repetição de sessão. Arize Phoenix (Elastic 2.0)  avaliações específicas de agentes profundas, relevância RAG, auto-instrumentamento OpenInference. Cometa Opik (Apache 2.0)  otimização automática de prompt, guardrails, detecção de alucinações de juízes LLM.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 14 · 23 (OTel GenAI) | **前置知识:** 见原文
**Time:** ~45 minutes | **时间:** 见原文

## Objetivos de aprendizagem

- Nomear as três principais plataformas de observação de agentes de código aberto e as suas licenças.
- Distinguir o que cada um é mais forte em: Langfuse (sessões de mgmt + rápida), Phoenix (RAG + auto-instrumentamento), Opik (optimização + guardrails).
- Explica por que 89% das organizações relatam ter observabilidade de agentes em vigor até 2026.
- Implementar um canal de rastreamento de dados de um sistema de dados com avaliação de juízes do MLL.

## O problema é o problema da introdução

OTel GenAI (Lessão 23) fornece o esquema. Você ainda precisa da plataforma que ingere intervalos, executa avaliações, armazena versões rápidas e superficia regressões.

> OTel GenAI ((第 23 课) deu-lhe um esquema. Você ainda precisa de uma plataforma para receber o tempo de execução, avaliação, armazenamento e apresentação de informações.

> - Não .**【前置】**O que é que é que é o que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é que é`invoke_agent`O que você pode fazer para entender o que é um LLM como um juiz é um modelo crítico, caso contrário, você vai julgar como "outro LLM" e não como "facto checagem baseada em evidências externas".


> **【中文解读】**A plataforma de observação de agentes fornece a capacidade de execução de agentes de um ponto a outro, desde o pedido do usuário até a resposta final.

## O conceito central.

### Langfuse (MIT)

> - Não .**【类比】**Três plataformas de observação como três tipos de sistemas de informação de hospitais:**Langfuse**é um hospital complexo HIS(住院、门诊、药房全打通tracing+prompt 管理+eval 一站式, enfatizando"you changed提示版本 v3 后,第三天崩的痕迹都能分到这个版本");**Phoenix**É um centro de inspecção especializada em RAG, que diz que o comportamento do agente não foi alterado, mas não importa qual a sua dica.**Opik**É um sistema de gestão de experimentos clínicos (A/B) que pode ser executado simultaneamente.

- 6M+ SDK instalações / mês, 19k+ estrelas GitHub.
- Características: rastreamento, gestão rápida com versão + playground, avaliações (LLM-as-judge, feedback do usuário, personalizado), repetições de sessão.
- Junho de 2025: módulos anteriormente comerciais (LLM-as-a-judge, filas de anotações, experimentos rápidos, Playground) de código aberto sob MIT.
- Forte para: observabilidade de ponta a ponta com um ciclo de gestão de prompt apertado.

### Arize Phoenix (Licença Elastica 2.0)

- Avaliação mais profunda específica do agente: aglomeração de vestígios, detecção de anomalias, relevância da recuperação para o RAG.
- Auto-instrumentamento nativo OpenInference.
- Pares com Arize AX gerenciado para produção.
- Não há versão rápida  posicionada como uma ferramenta de deriva/regressão comportamental ao lado de plataformas mais amplas.
- Forte para: relevância RAG, deriva comportamental, detecção de anomalias.

### Cometa Opik (Apache 2.0)

- Otimizar imediatamente automaticamente através de experimentos A/B.
- Os limites de segurança (redagamento de PII, restrições tópicas).
- Juez de LLM detecção de alucinações.
- Benchmark da própria medição do Comet: Os registros de Opik + avaliações em 23.44s vs Langfuse 327.15s (~ 14x gap)  tomam os benchmarks do fornecedor como direcionais.
- Forte para: ciclo de otimização, experimentação automatizada, aplicação de barrancos.

### Dados da indústria

Por Maxim (2026 análise de campo): 89% das organizações têm observabilidade de agentes em vigor; os problemas de qualidade são a principal barreira à produção (32% dos entrevistados citam-nos).

> A plataforma de rastreamento de agentes é a principal ferramenta de rastreamento de agentes em 2026:

### Escolhendo um

| Need | Pick |
|------|------|
| All-in-one with prompt management | Langfuse |
| Deep RAG evaluation + drift | Phoenix |
| Automated optimization + guardrails | Opik |
| Open licensing, no ELv2 | Langfuse (MIT) or Opik (Apache 2.0) |
| Datadog / New Relic integration | Any — they all export OTel |

### Onde este padrão vai mal

> 🤔 **【困惑】**P: 89% das organizações dizem que têm um agente observavel, mas por que o acidente ainda existe? A: A maioria das equipes só fez "contact OTel → trace into Langfuse" esta etapa, é como instalar uma câmera de monitoramento, mas ninguém vê.

- **No eval strategy.**O rastreamento sem avaliação é apenas uma exploração caríssima.
- **Self-rolled LLM-judge without grounding.**Aplica-se o padrão CRITICO (LECÇÃO 05)  os juízes precisam de ferramentas externas para a verificação factual.
- **Prompt versions not tied to traces.**Quando o prod regressar, não se pode dividir para o impulso que o causou.

> **没有评估策略。**Não há nenhuma avaliação, apenas um caro diário.
> **自建的 LLM 评审器没有基础。**O método crítico é o método utilizado para a análise de dados.
> **提示版本未与追踪关联。**Quando a produção regressar, você não pode se posicionar para o problema.

## Construí-lo e realizei-o.

> ️ **【易错点】**场景: equipe colocou OTel trace 接到 Langfuse 后, escreveu um jurado LLM 给每条 trace 打 1-5 分, mas rubrica apenas uma frase "responde bem mal" → 后果:分数毫无意义, judge Colocar" cortesia mas responder errado "打 5 分"",correto mas breve"打 2 分,dashboard 上 95% 满意度但客户投诉暴 → 修复:rubrica 必须分维维度((factual correctness、scope adherence、tone), por dimensão de operação falha definição (((就是 "scope adherence:
```figure
wb-trace-ingest
```

## Construí-lo

`code/main.py`Implementa um colecionador de vestígios stdlib + avaliador de juízes LLM:

> A plataforma de rastreamento de agentes é a principal ferramenta de rastreamento de agentes em 2026:

- Ingerir espessuras em forma de GenAI.
- Grupo por sessão, etiqueta de corridas falhadas (viagens de guarda-roupa, avaliações de baixa confiança).
- Um juiz de LLM com guião que marca as respostas dos agentes em uma rubrica.
- Um resumo semelhante a um painel de instrumentos: taxa de falhas, principais razões de falhas, distribuição de pontuação de avaliação.

- É o que é ?

```
python3 code/main.py
```

Resultado: pontuações de avaliação por sessão e categorização de falhas correspondentes ao que mostraria a Langfuse/Phoenix/Opik.

> 输出: por reunião, avaliação de cada reunião, correspondência Langfuse/Phoenix/Opik

> A plataforma de rastreamento de agentes é a principal ferramenta de rastreamento de agentes em 2026:

## Use-o com o framework implementado.

- **Langfuse**Auto-hosted ou em nuvem; via via OTel ou o seu SDK.
- **Arize Phoenix**Auto-hosted; auto-instrument OpenInference.
- **Comet Opik**Auto-hosted ou em nuvem; ciclo de otimização automatizado.
- **Datadog LLM Observability**Para equipes de operações mistas + ML que já executam o Datadog.

## Envia-o . Produto .

`outputs/skill-obs-platform-wiring.md`escolhe uma plataforma e traça + avalia + solicita versões para um agente existente.

> `outputs/skill-obs-platform-wiring.md`选择一个平台,并将追踪 + 评估 + 提示版本接入现有代理──

> A plataforma de rastreamento de agentes é a principal ferramenta de rastreamento de agentes em 2026:

## Exercícios.

1. Exportar uma semana de rastreamentos do OTel para a nuvem Langfuse.
  Tradução do inglês para tradução do inglês:
2. Escreva uma rubrica de juiz de LLM para o seu domínio (correção factual, tom, adesão ao escopo).
  Tradução do inglês para tradução do inglês:
3. Comparar a versão de Lanfuse com a aglomeração de rastreamentos da Phoenix.
  Tradução do inglês para tradução do inglês:
4. Leia os documentos do barranco do Opik, entregue um barranco de redação de informações a um dos seus agentes.
  Tradução do inglês para tradução do inglês:
5. Marque os três no seu corpus, ignore os números publicados pelo fornecedor, mensure os seus.
  Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|---|
| Tracing | "Spans collector" | Ingest OTel / SDK spans; index by session |  |
| Prompt management | "Prompt CMS" | Versioned prompts tied to traces |  |
| LLM-as-judge | "Automated eval" | Separate LLM scores agent output against a rubric |  |
| Session replay | "Trace playback" | Step through past runs for debugging |  |
| RAG relevancy | "Retrieval quality" | Does the retrieved context match the query |  |
| Trace clustering | "Behavioral grouping" | Cluster similar runs for drift detection |  |
| Guardrail enforcement | "Policy at log time" | PII/toxicity/scope checks on logged content |  |

## Mais leitura 延伸阅读

- [Langfuse docs](https://langfuse.com/) rastreamento, avaliações, urgência
  Tradução do português:
- [Arize Phoenix docs](https://docs.arize.com/phoenix) Auto-instrumentamento, derivação
  Tradução do português:
- [Comet Opik](https://www.comet.com/site/products/opik/) Optimização + barris
  Tradução do português:
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) o esquema todos os três consumir
  Tradução do português:
