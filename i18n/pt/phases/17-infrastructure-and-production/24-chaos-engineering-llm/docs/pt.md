# Chaos Engineering para LLM Production 工程 生产 混沌 LLM

> A engenharia do caos para LLM é sua própria disciplina em 2026. Preerequisito antes de executar experimentos em produção: SLI/SLO definido, observabilidade de rastreamento+metrico+log, retrocesso automatizado, runbooks, em chamada. A arquitetura tem quatro planos: controle (programador de experimentos), alvo (serviços, infra, armazéns de dados), segurança (guardas + abortos + filtros de tráfego), observabilidade (metricas + vestígios + registros), feedback (em ajustes SLO). Os guardrails são obrigatórios: alertas de taxa de queimação interrompem os experimentos se se espera que a queima diária de erro-orçamento > 2x; janelas de supressão + correlação de rastreamento-ID dedupção de ruído de alerta. Cadência: revisão semanal de pequenas canárias + SLO; dia de jogo mensal + pós-mortem; auditoria trimestral de resiliência entre equipes + mapeamento de dependência. Experimentos específicos do LLM: sobrecarga de memória, falhas de rede, interrupções de fornecedores, instruções malformadas, tempestades de despejo de cache KV. Ferramentas: Engenharia de Caos de Aproveitamento (recomendações derivadas do LLM, redução do raio de explosão, integração de ferramentas MCP); LitmusChaos (CNCF); Chaos Mesh (nativa do Kubernetes do CNCF).

> **【中文解读】**Esta secção apresenta a prática do LLM 混沌工程主动注入故障来测试 LLM 服务性的实践──


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy chaos experiment runner) | **语言:** Python
**Prerequisites:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability)

> - Não .**【前置】**O curso de Estudos em Ciências Sociais e Ciências Sociais (SES) é uma disciplina de ensino superior que inclui a formação de um profissional de ensino superior.
> - Não .**【类比】**LLM 混沌工程 = "Exercícios de fogo"。前提:SLI/SLO 定义好、可观测、自动回滚、runbook、on-call。四平面:控制(实验调度) + objetivos(服务/数据/基础设施) + segurança(守卫/中止/流量过) +可观测。必须护:错误预算燃烧率 > 2x 时暂停实验──节奏:每周小卡纳里度+月度游戏日+季度跨团队审计──LLM 专属实验:内存过载、网络故障、供应商 机、坏快点、KV cache 驱逐风暴──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Objetivos de aprendizagem

- Cite os cinco requisitos prévios de engenharia do caos (SLI/SLO, observabilidade, retrocesso, runbooks, on-call) e explique por que saltar qualquer um rompe a prática.
  Tradução do inglês para o português: ︎ ︎
- Diagrama os quatro planos (controle, alvo, segurança, observabilidade) e o ciclo de feedback em SLO.
  Tradução do inglês para tradução do inglês: draw four planes (control, goal, safety, observação) e reversão do ciclo até o painel de instrumentos SLO.
- Cite cinco experimentos específicos do LLM (supercarga de memória, falha da rede, interrupção do fornecedor, aviso mal formado, tempestade de despejo de KV).
  Chinese: 列举五个 LLM 特定混沌实验 (LEM) 列举五个 LLM 特定混沌实验 (LEM) 列举五个 LLM 特定混沌实验 (LEM) 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个 LLM 列举五个LEM 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列举 列 列举 列举 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 列 
- Escolha uma ferramenta  Arnes, LitmusChaos, Chaos Mesh  dado pilha.
  中文翻译:选择工具Harness、LitmusChaos、Chaos Mesh根据技术。

## O problema é o problema da introdução

> **【中文解读】**LLM 混沌工程是2026年的独立学科──LLM 增加了新的故障模式:4K-token 的毒化字符使分词器卡住12秒;上游提供商 429 触发网关重试,重试放大并发导致OOM;突发负载下 KV Cache 淘汰风暴引发重填级联,耗尽计算资源──这些都不会出现单元测试中混沌工程工具直到用户发现它们的方法──

> **【拓展：LLM 混沌工程的五类实验】**2026 LLM 特定五类混沌实验:(1) 内存过载发送长上下文高并发请求引发 KV Cache 抢占风暴,观察服务是优雅降级还是崩;(2) 网络故障断断推理网关与供应商的连接,观察故障是否在SLA内生效;(3) 供应商中断模拟100% OpenAI 429,观察路由是否失败到Antropic;(4) 形提示注入死载分层嵌套 Unicode、UTF-8码点卡),观察单个请求锁住员工淘汰;5) KV 淘汰巨大暴风和vLLM 块预算强制淘汰, L L L 恢复服务MC 强制淘汰, L 恢复 恢复 查看.

O teste de caos nas pilhas tradicionais é estabelecido. As pilhas LLM adicionam novos modos de falha. Um prompt de token 4K com um caracter venenoso impede o tokenizer por 12 segundos. Um provedor upstream 429s; sua gateway retries; seus OOMs de serviço em simultâneo amplificado retry. Uma tempestade de despejo de cache KV sob carga de explosão causa cascas de preenchimento que saturam a computação.

A engenharia do caos é a forma de descobri-las antes que os usuários o façam.

## O conceito central.

### Pre-requisitos

> **【中文解读】**Em produção, é executado um teste de caos com cinco pressupostos: 1) SLI/SLO 已定义; 2) 可观测性(trace + metric + log) já implantado; 3) 自动回滚机制就绪; 4) 结构化 runbook 已编写; 5) 有值班人员响应──缺少任何一项,混沌就会变成真实事件──四个平面:控制面(实验调度机) 目标面服务/基础设施) 安全、面杀开机 + 抑制窗口 + 爆炸射线 限制) 、观测面标签 + 关键 关键 关键) 反循环将发现可回到 SLO 调整、运行 更新和代码书修复──

Não faça caos na produção sem:

1. **SLI/SLO** definidos indicadores e objectivos de nível de serviço.
2. **Observability**Traços, métricas, registos, ligados a painéis de controlo.
3. **Automated rollback** Fase 17 · 20 Rolo de volta à política de bandeira.
4. **Runbooks** estruturada, fase 17 · 23.
5. **On-call**- Alguém para responder.

Faltando qualquer meio, o caos torna-se um incidente real.

### Quatro aviões + feedback

**Control plane** programação de experiências (fluxo de trabalho de Litmus, programação Chaos Mesh, UI Harness).

**Target plane**Serviços, cápsulas, nós, balançadores de carga, armazéns de dados.

**Safety plane**- interruptor de eliminação, janelas de supressão, limites de raio de explosão, portões de orçamento de erro.

**Observability plane** métricas normais + correlação de rastreamento de identificação para distinguir os erros induzidos pelo caos e os erros naturais.

**Feedback loop** Os resultados são repassados para o ajuste do SLO, atualizações do cadastro de execução, correções de código.

### Os corredores são obrigatórios

> **【拓展：混沌工程的安全护栏】**Os três requisitos de segurança necessários para o processo de desorganização: 1) a taxa de queimação máxima de alarmes durante os experimentos se o gasto diário de erros orçamentais for superior ao esperado em 2x, o desorganização automático dos experimentos; 2) a inibição de janelas em um raio de explosão do experimento, a silêncio não experimental, a evitar ruído em ligação; 3) o rastreamento de identificação de todos os experimentos causados por erros, que o desorganização possa ser repetido.

- **Burn-rate alert**A redução da taxa de erro de orçamento diário é de 2x a esperada.
- **Suppression windows**: silenciar as alertas não experimentais no raio da explosão durante o experimento.
- **Trace-ID correlation**Todos os erros induzidos pela experiência têm uma etiqueta para que a chamada possa deduzir.

### Cinco experiências específicas de LLM

1. **Memory overload** forçar uma tempestade de prevenção do cache KV enviando solicitações de longo contexto com alta concurência. Observe: o serviço desce graciosamente ou falha?

2. **Network failure** cortar a conectividade entre o gateway de inferência e o provedor.

3. **Provider outage simulation** 100% 429 da OpenAI. Observação: faz o roteamento falhar para Anthropic? (fase 17 · 16, 19)

4. **Malformed prompt** injectar carga útil de instalação de tokenizer (por exemplo, unicode profundamente aninhado, um enorme código UTF-8). Observe: um único pedido bloqueia um trabalhador?

5. **KV eviction storm**Observe: a LMCache recupera ou o serviço deteriora?

### Cadência

- **Weekly**- Pequenas experiências de canários em fase, talvez 5% de prod.
- **Monthly** dia de jogo programado num cenário específico; participação de equipas cruzadas; pós-mortem.
- **Quarterly** Auditoria de resiliência entre equipes; atualização do mapa de dependência.

### Ferramentas

> **【拓展：混沌工程工具选择】**2026 anos de confusão engenharia ferramenta seleccion:(1) Harness Chaos Engineering商业,AI 驱动的实验推,blast radius 自动缩放,MCP 工具集成;(2) LitmusChaosCNCF 毕业,Kubernetes 工作流式;(3) Chaos MeshCNCF 沙箱,Kubernetes-native CRD风格;(4) Gremlin商业,广泛支持;(5) AWS FIS / Azure Chaos Studio托管云服务;;节奏建议:每周小卡纳里 实验 + SLO 审查,每月游戏日 + 后期,每季度跨团队性审计 + 依赖映射更新;;

- **Harness Chaos Engineering** comercial; recomendações de experiências derivadas da IA; redução da escala do raio de explosão; integração de ferramentas MCP.
- **LitmusChaos** Graduado no CNCF; Kubernetes baseado no fluxo de trabalho.
- **Chaos Mesh** caixa de areia CNCF; estilo CRD nativo Kubernetes.
- **Gremlin** comercial; amplo apoio.
- **AWS FIS**- Não .**Azure Chaos Studio** Ofertas em nuvem gerenciadas.

### Começando pequeno

Primeiro experimento: matem uma réplica de decodificação sob tráfego constante, observem o redirecionamento e a recuperação, se isto funcionar e parecer seguro, passam para o caos da rede.

Primeiro experimento específico do LLM: injetar um fornecedor 429 por 5 minutos. Observe o retorno. A maioria das equipes descobre que o retorno não foi totalmente testado.

### Números que você deve lembrar

- Quatro aviões: controlo, alvo, segurança, observabilidade.
- Pausa de taxa de queima: 2x a queima de orçamento diário esperada.
- Cadência: canário semanal, dia de jogo mensal, auditoria trimestral.
- Cinco experiências de LLM: memória, rede, provedor, prompt malformado, KV tempestade.

## Use-o com o framework implementado.
```figure
i4-chaos-guard
```

## Usá-lo

`code/main.py`Simula três experimentos de caos com portões de segurança, relatos de quais experimentos poderiam tropeçar o aborto de queimadura.

> `code/main.py`Simula três experimentos de caos com portões de segurança, relatos de quais experimentos poderiam tropeçar o aborto de queimadura.

> `code/main.py`Simula três experimentos de caos com portões de segurança, relatos de quais experimentos poderiam tropeçar o aborto de queimadura.

## Envia-o . Produto .

Esta lição produz`outputs/skill-chaos-plan.md`- Dada a pilha e a maturidade, escolhe os três primeiros experimentos e as ferramentas.

> 本课产 出 `outputs/skill-chaos-plan.md`- Dada a pilha e a maturidade, escolhe os três primeiros experimentos e as ferramentas.

## Exercícios.

1. Corra .`code/main.py`Qual experimento desacelera o portão de velocidade e porquê?
   Tradução: 运行`code/main.py`Qual experimento provocou a taxa de queimação?
2. Desenhar as cinco primeiras experiências de caos para um serviço RAG baseado em vLLM. Incluir critérios de sucesso.
   Tradução do inglês para "Rag Service Design"
3. O seu alerta de taxa de queimação parou um experimento.
   Tradução do inglês: Your burning rate report police suspended an experiment. Como determinar o comportamento da causa contra o comportamento esperado?
4. Discutir se o caos deve correr na produção ou apenas em cena.
   O que é que é o ambiente de produção?
5. Cite três modos de falha específicos do MLC que o caos genérico da rede não pode reproduzir.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SLI / SLO | "service targets" | Indicator + objective; required prerequisite |
| Blast radius | "scope" | Set of services / users affected by experiment |
| Burn-rate alert | "budget gate" | Fires when error-budget burn rate > 2x expected |
| Game day | "monthly drill" | Scheduled cross-team chaos exercise |
| LitmusChaos | "CNCF workflow" | Graduated CNCF Kubernetes chaos tool |
| Chaos Mesh | "CNCF CRD" | CNCF sandbox Kubernetes-native chaos |
| Harness CE | "commercial AI-assisted" | Harness chaos with AI recommendations |
| Malformed prompt | "tokenizer bomb" | Input that stalls tokenization |
| KV eviction storm | "preemption cascade" | Mass eviction triggering re-prefills |

## Mais leitura 延伸阅读

- [DevSecOps School — Chaos Engineering 2026 Guide](https://devsecopsschool.com/blog/chaos-engineering/)
- [Ankush Sharma — Observability for LLMs (book)](https://www.amazon.com/Observability-Large-Language-Models-Engineering-ebook/dp/B0DJSR65TR)
- [LitmusChaos (CNCF)](https://litmuschaos.io/)
- [Chaos Mesh (CNCF)](https://chaos-mesh.org/)
- [Harness Chaos Engineering](https://www.harness.io/products/chaos-engineering)
- [AWS FIS](https://aws.amazon.com/fis/)
