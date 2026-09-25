# Tráfico de Sombras, Canary Rollout e implantação progressiva para LLM

> Os implementos LLM combinam as partes mais difíceis da implantação de software: não existem testes unitários, modos de falha difusos, sinais atrasados. A sequência é (1) modo sombra  pedidos duplicados de prod para modelo candidato, registro, comparação com impacto zero do usuário; pega problemas óbvios de distribuição, mas não é uma garantia de qualidade; (2) implantação canária  mudança progressiva de tráfego 10% → 25% → 50% → 75% → 100% com portas em cada etapa; percentilhas de latência de rastreamento, custo / pedido, taxa de erro / recusa, distribuição de comprimento de saída, taxa de feedback do usuário; (3) testes A / B para alternativas distintas após a estabilidade confirmar. O não-determinismo é irredutível  variação de precisão de até 15% em corridas com entradas idênticas devido à não-asociabilidade do GPU FP mais variação de tamanho de lote. O custo é variável, não constante  um modelo 20% melhor pode ser 3x mais caro por chamada. A velocidade de retorno é decisiva: se o retorno requer uma redeplocação, é muito lento. Política vive em configuração/flag; modelo vive em registro com digestões fixas; rollback = política de reversão + limiar de reversão + pin modelo antigo em segundos.

> **【中文解读】**Este capítulo apresenta os estratégias de implementação da Shadow / Kinshe Narr / Gradual Deployment LLM  Serviços de Segurança na Internet.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy canary-progression simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 21 (A/B Testing)

> - Não .**【前置】**O programa é um dos mais difíceis de implementar.
> - Não .**【类比】**LLM 部署三步 = "飞机首飞流程"。 Shadow = 地面模拟(复制 prod Petição, 零用户影响, 对比但不切换);Canary = 真飞但逐步开载客(10%→25%→50%→50%→100%, cada passo有门禁);A/B = 商务航班对比(稳定测不同方案)。关键后:非确定性不可消除(GPU 浮点+batch 差异致 15% 准确率波动); custo é variação(good 20% de modelos podem ser caros 3 倍); segundos de velocidade de rotação determinante(segundo de classificação 切换不能重新部署)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Distinguir o modo sombra (comparar com impacto zero), canário (trafego ao vivo progressivo) e A/B (comparar confirmado pela estabilidade).
  Chinese Translation:区分影子模式 (区分影子模式) 零影响比较) 金丝雀 (金丝雀) 真实流量渐进 (真流量渐进) 和 A/B (统计比较) ⋅
- Cite cinco métricas canárias específicas do MLL (latença, custo/requisito, erro/recusão, distribuição de comprimento de saída, feedback do utilizador).
  Chinese: 列举五个 LLM 特定金丝雀指标(延迟、成本/请求、错误/拒绝、输出长度分布、语义质量样本)
- Explique por que o não-determinismo do MLL (até 15%) muda o que significa "estavel" numa implantação.
  Tradução do inglês para tradução do inglês: explains why LLM não determinação (高达15%) altered the meaning of "stabilisation" in the introduction.
- Desenhar um caminho de retrocesso que leve segundos (flip de política) e não horas (redistribuição).
  Chinese: 设计一个秒级回滚路径 (设计一个秒级回滚路径),而非小时级 (设计一个秒级回滚路),而不是小时级 (设计一个秒级回滚路),而不是小时级 (设计一个秒级回滚路),而不是小时级 (设计一个秒级重新部署)

## O problema é o problema da introdução

> **【中文解读】**A LLM 部署 部署结合软件部署中最难的部分:没有单元测试、模糊的失败模式、延迟的信号──正确序列是:(1) 影子模式将生产请求复制到候选模型,日志对比,零用户影响;(2) 金丝雀发布10%→25%→50%→75%→100% 渐进流量切换,每个阶段有门控标;(3) A/B 测试稳定性确认后的比比比比──回滚速度是决定性的策略标志翻转(30秒)vs 重部署(3 小时)

> **【拓展：LLM 非确定性与部署】**A incerteza do LLM é inconstitucional o mesmo input no mesmo modelo pode produzir até 15% de diferença de precisão de taxa de erro.

Enviamos um novo modelo, as avaliações offline mostram um aumento de 3% de precisão, e depois o colocamos em produção, dentro de 24 horas, o custo aumenta 40%, os dedos do usuário aumentam 8%, três bilhetes de clientes relatam respostas estranhas.

Cada peça disso era evitável. O modo sombra teria pegado o aumento de 40% antes que qualquer usuário o visse. Canary teria parado em 10% quando os polegares baixaram. O retorno da bandeira política teria demorado 30 segundos. A disciplina é o que preenche o fosso entre "a avaliação offline parece boa" e "os usuários reais estão felizes".

## O conceito central.

### Modo de sombra

> **【中文解读】**影子模式候选模型接收与生产相同的请求,输出仅记录不回归用户――日志内容包括:输出内容(与生产不同) 代码数量(成本差异)、延迟、拒绝和错误――能捕获:成本爆炸、长度退化、明显拒绝变化、硬错误――不能捕获:用户会感知到质量差异影子是烟雾测试,不是质量测试――

O candidato recebe as mesmas solicitações que a produção; as saídas são registradas, não devolvidas aos usuários.

- Conteúdo de produção (diferência em relação à produção).
- Contas de tokens (delta de custo).
- - A latência.
- Rejeição e erro.

Captures: custos aumentados, regressões de comprimento, mudanças óbvias de recusa, erros difíceis. NÃO captura: qualidade que os usuários do delta perceberiam.

### Lançamento das Canárias

> **【拓展：LLM 金丝雀发布的五个门控指标】**O LLM 金丝雀 lançou cinco indicadores de controle obrigatórios: 1) 延迟百分位(P50/P95/P99) Canary P99 > 1.5x 基线则触发; 2) Cada pedido custo>20% 高于基线则触发; 3) 错误/拒绝率2x 基线则触发; 4) 输出长度分布均值 + P99 分布偏移值则触发; 5) 用户反率指下/工单 1.5x 基线则触发;; típico progresso 1%→10%→25%→50%→75%→100%, cada fase acumulado suficiente para 5-15 minutos de exame de intervalo)

Progresso do tráfego com portões. Progressão típica: 1% → 10% → 25% → 50% → 75% → 100%. Portão em 5 métricas em cada etapa:

1. **Latency percentiles** P50, P95, P99. violação: canário tem P99 > 1,5x de linha de base.
2. **Cost per request** misturado.
3. **Error / refusal rate**5xx mais recusas explícitas.
4. **Output length distribution** média + P99. violação: deslocamento distributivo.
5. **User-feedback rate**- Infração: 1,5x da linha de base.

### O não-determinismo é a nova variância

As entradas idênticas produzem saídas não idênticas.

- Não-asociabilidade do GPU FP (ordem de redução de ponto flutuante varia de acordo com o lote).
- Variância de tamanho do lote (a mesma solicitação num lote de 128 versus um lote de 16).
- Amostragem (temperatura > 0).

Medido: variação de precisão de até 15% em conjuntos de avaliação idênticos. "Stable" num lançamento significa que as métricas estão dentro da variância esperada, não idênticas à linha de base.

### O custo é uma variável

Um modelo 20% melhor pode ser 3 vezes mais caro por chamada. custo/requisito é um dos cinco portões. Envio de um modelo "melhor" que quebra a economia de unidade é um caso de retrocesso.

### O Rollback é a arma.

- Flagão de política (sistema de flag de características): porcentagem de desvio em configuração; demora segundos.
- Modelo de fixação (digestão do registo): o modelo fixa não se actualiza automaticamente.
- Rollback = reverter a bandeira + definir digestado fixado para o anterior.

Se a pilha precisar de ser redistribuída para o rollback, corrija-a antes de rolar.

### Ferramentas

> **【拓展：LLM 渐进式部署工具链】**Seleção de ferramentas para a implementação do programa de licenciatura em 2026: 1) Argo Rollouts / FlaggerKubernetes 原生渐进式部署控制器,与 Istio/Linkerd 加权路由集成; 2) Istio ponderada routing服务网格级流量切分; 3) KServe / Seldon Core模型服务自带卡纳里功能; 4) FlagsLaunchDarkly、Flagsmith、Unleash, strategy class翻转无需重新部署──回滚基础设施:策略标志标志功能系统)翻转百分比在配置中秒级) 模型注册摘录固定pinged digest 不自动升级)  Se você precisar de um novo depósito de dados, começa novamente a redirecionar essa linha.

**Argo Rollouts**- Não .**Flagger** Controllers de entrega progressivos Kubernetes. Integrados com roteamento ponderado Istio/Linkerd.

**Istio weighted routing** Divisão do tráfego a nível de rede de serviços.

**KServe / Seldon Core** modelo servindo com canário incorporado.

**Feature flags**Lançamento: Darkly, Flagsmith, Unleash.

### Cadência de métricas

Canary gates verifica a cada 5-15 minutos dependendo do volume de tráfego. 1% do tráfego com 10 req / min dá 50-150 pontos de dados por janela  suficiente para latência, mas barulhento para o feedback do usuário. 10% dá ~ 10x mais.

### O passo A/B é opcional

Se o novo modelo é claramente diferente (comportamento diferente, curva de custo diferente, tom diferente), teste-o A/B em 50% após canário passar.

### Números que você deve lembrar

- Progressão canária: 1% → 10% → 25% → 50% → 75% → 100%.
- O limite máximo de não-determinismo: até 15% de variação corrida para corrida em insumos idênticos.
- Cinco métricas canárias: latência, custo, erro/recusão, comprimento de saída, feedback do utilizador.
- Por exemplo, o valor de um produto em causa é de 20% ou mais.
- Segundo, não horas.

## Use-o com o framework implementado.
```figure
i4-canary-ramp
```

## Usá-lo

`code/main.py`Simula uma implantação de canários com regressões injetadas.

> `code/main.py`Simula uma implantação de canários com regressões injetadas.

> `code/main.py`Simula uma implantação de canários com regressões injetadas.

## Envia-o . Produto .

Esta lição produz`outputs/skill-rollout-runbook.md`. Tendo em conta o modelo candidato, a linha de base e a tolerância ao risco, desenha um plano shadow→canary→100%.

> 本课产 出 `outputs/skill-rollout-runbook.md`. Tendo em conta o modelo candidato, a linha de base e a tolerância ao risco, desenha um plano shadow→canary→100%.

## Exercícios.

1. Corra .`code/main.py`Injectar uma regressão de 25% dos custos.
   Tradução: 运行`code/main.py`Injectar 25% de seu rendimento. Em que estágio o captura?
2. O seu novo modelo tem 3% de precisão ganho offline mas custo/requisito é +18%. É um navio?
   Tradução do inglês:Do teu novo modelo a precisão de saída aumentou 3% mas o custo/requisito +18%
3. Desenhe um rollback que leve menos de 60 segundos de ponta a ponta.
   Tradução do inglês: design端到端 60 秒内回滚──列出所需基础设施──
4. Não-determinismo mostra ±7% na sua avaliação.
   Chinese: 不确定性显示 +/-7%──设金丝雀门控以避免误报──
5. O modo sombra aumenta o custo de 40% antes do canário.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Shadow mode | "duplicate to new" | Zero-impact send-to-candidate for logging |
| Canary | "progressive traffic" | Gradual user-exposed rollout with gates |
| Gates | "rollout checks" | Metric thresholds that block progression |
| Non-determinism | "LLM variance" | Irreducible run-to-run differences |
| Policy flag | "flag flip rollback" | Config-level rollback, seconds not hours |
| Model pin | "registry digest" | Immutable reference to a model version |
| Argo Rollouts | "K8s progressive" | Kubernetes-native canary/rollback controller |
| KServe | "inference K8s" | Model serving with canary primitives |
| Istio weighted | "mesh split" | Service-mesh traffic splitter |

## Mais leitura 延伸阅读

- [TianPan — Releasing AI Features Without Breaking Production](https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing)
- [MarkTechPost — Safely Deploying ML Models](https://www.marktechpost.com/2026/03/21/safely-deploying-ml-models-to-production-four-controlled-strategies-a-b-canary-interleaved-shadow-testing/)
- [APXML — Advanced LLM Deployment Patterns](https://apxml.com/courses/mlops-for-large-models-llmops/chapter-4-llm-deployment-serving-optimization/advanced-llm-deployment-patterns)
- [Argo Rollouts docs](https://argo-rollouts.readthedocs.io/)
- [Flagger docs](https://docs.flagger.app/)
