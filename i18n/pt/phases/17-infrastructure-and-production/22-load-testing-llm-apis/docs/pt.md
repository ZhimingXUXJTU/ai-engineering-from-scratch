# Load Testing LLM APIs  Por que K6 e Locust mentem  Load Test API 

> Os testadores de carga tradicionais não foram projetados para respostas de streaming, comprimentos de saída variáveis, métricas de nível de token ou saturação de GPU. Duas armadilhas mordem a maioria das equipes. A armadilha do GIL: A medição de nível de tokens do Locust executa a tokenização sob o Python GIL, que compete com a geração de solicitações sob alta concurência; o backlog da tokenização então infla a latência entre tokens relatada. A armadilha de uniformitade de prompt: as mesmas instruções em um loop testam um ponto na distribuição do token; o tráfego real tem comprimento variável e diferentes correspondências de prefixos. A LLMPerf resolve isto com `--mean-input-tokens`+ `--stddev-input-tokens`. Mapeamento de ferramentas em 2026: especializado em LLM (GenAI-Perf, LLMPerf, LLM-Locust, guidellm) para a precisão de tokens; **k6 v2026.1.0**+ **k6 Operator 1.0 GA (Sept 2025)** streaming-consciente, Kubernetes-nativo distribuído através de testRun/PrivateLoadZone CRDs, melhor para portões CI/CD; Vegeta for Go saturação de taxa constante; Locust 2.43.3 apenas com extensão LLM-Locust para streaming. padrões de carga: estádio, rampa, pico (test de autoescalação), remoção (vazes de memória).

> **【中文解读】**Este capítulo apresenta o método de teste de desempenho da API de LLM carga de teste  avaliação de sugestões de serviço em alta carga 


**Type:** Build | **类型:** 学习
**Languages:** Python (stdlib, toy realistic-prompt generator + latency collector) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling)

> - Não .**【前置】**学本节前请先掌握:Fase 17·08(指标)、Fase 17·03(GPU 扩缩)。
> - Não .**【类比】**LLM 负载测试 = "测自动驾驶 vs 测传统车"──两个陷:(1) GIL 陷:Locust 在 Python GIL 下做代币化,与请求生成抢锁→报告的代币 间延迟虚高(客户端是瓶不是服务端);(2) Prompt 一致性陷:循环同步 快速只测分布一个点,真流量有多样化前匹配──LLMPerf 用 `--mean-input-tokens+stddev`修复──2026 工具:GenAI-Perf/LLMPerf/LLM-Locust(LLM 专用) + k6 v2026.1(流式+K8s) + Vegeta(Go 常速率) + Locust(仅配 LLM-Locust 扩展)
**Time:** ~75 minutes | **时间:** ~75 minutes

## Objetivos de aprendizagem

- Explique os dois padrões anti-patrões (trampa GIL, armadilha de uniformidade de ponta) que fazem os testadores de carga genéricos mentir para as API de LLM.
  Tradução do inglês para tradução inglesa: explicar dois métodos de teste de carga (GIL)
- Escolha uma ferramenta para um determinado propósito: LLMPerf (exercício de referência), extensão de streaming k6 + (gate CI), guidellm (sintetico em larga escala), GenAI-Perf (referência NVIDIA).
  中文翻译:选择工具Harness、LitmusChaos、Chaos Mesh根据技术。
- Desenhe quatro padrões de carga (estabilização, rampa, ponta, remoção) e nomeie o modo de falha de cada captura.
  Chinese Language Translation: Design Four Sorts of Load Models (Desenho de quatro tipos de carga)
- Construir uma distribuição realista de prompt usando média + stddev de tokens de entrada em vez de comprimento fixo.
  Tradução do inglês: Using输入 token 的平均值 + 标准差构建真实提示分布,而非固定长度──

## O problema é o problema da introdução

> **【中文解读】**传统负载测试工具不是为 LLM设计的它们不支持流式响应、可变输出长度、代码级指标或GPU 和度。两个常见陷:(1) GIL 陷Locust 代码级测量在Python GIL 下运行分词,高并发时代代码化 队列膨胀,虚报 延迟 ((tuas clientes端是瓶,不是服务器);2) 均性陷循环测试中使用相同提示,前缓存中命率接近100%,吞吐量看起来很好但完全不反映真实流量;;

> **【拓展：LLM 负载测试的四种模式】**2026 ano LLM  carga teste de quatro tipos: 1) estável  estável  estável RPS continuo 30-60 minutos, captura de função de linha de base degradada; 2) 渐增                                                                                                                                                                                                                                       

Você testou o seu endpoint LLM em 500 usuários simultâneos. Ele funcionou. Você enviou. Na produção em 200 usuários reais o serviço caiu sobre P99 TTFT explodiu, GPUs fixados.

Dois coisas aconteceram. Primeiro, k6 enviou 500 instruções idênticas  a sua coleta de solicitações e o cache de prefixos fizeram parecer que você estava a lidar com 500 decódios simultâneos quando você estava realmente a lidar com um. Segundo, k6 não rastreia a latência entre tokens nas respostas de streaming da maneira como o olho a experimenta; vê uma conexão HTTP, não 500 tokens chegando em intervalos variados.

O teste de carga para LLM é sua própria disciplina.

## O conceito central.

### A armadilha do GIL (Locust)

> **【拓展：Python GIL 对 LLM 负载测试的影响】**Python GIL(全局解释器锁) Efeito do teste de carga em LLM:Locust Use Python 运行客户端分词,在高并发时代代代码化 队列排在请求生成后面── 报告的间代码 延迟包含客户端代码化 积压你以为是服务器慢,其实是测试工具的瓶──解决方案:(1) LLM-Locust 扩展将代码化 移到独立进程;(2) 使用编译语言工具kkk) rfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

Locust usa Python e executa o lado do cliente de tokenização sob o GIL. Em alta concurência, as filas de tokenização por trás da geração de solicitações. A latência entre tokens relatada inclui o backlog de tokenização do lado do cliente. Você acha que o servidor é lento; é o teste de uso.

Correção: A extensão LLM-Locust muda a tokenization para processos separados, ou usa um harness compilado de linguagem (k6, LLMPerf usando tokenizers.rs).

### A armadilha da uniformidade rápida

Todos os testadores de carga conhecidos permitem configurar um prompt. Em um teste de loop de 10.000 iterações, o mesmo prompt exatamente é enviado cada vez. O servidor vê o mesmo prefixo cada vez que o prefixo  bate no cache perto de 100%, o throughput parece ótimo.

Fix: amostra de uma distribuição rápida.`--mean-input-tokens 500 --stddev-input-tokens 150` Diversos comprimentos, conteúdo diversificado.

### Quatro padrões de carga

1. **Steady-state** RPS constante durante 30 a 60 minutos.
2. **Ramp** aumentar linearmente o RPS de 0 para o objectivo durante 15 minutos.
3. **Spike**- Repentinamente 3-10x RPS durante 2 minutos e depois de volta.
4. **Soak**- estado de estabilidade durante 4-8 horas. Captura: vazamentos de memória, deriva do pool de ligação, sobreposição de observabilidade.

### 2026 mapeamento de ferramentas

> **【中文解读】**2026 ano LLM 负载测试工具选择:(1) LLMPerf(Anyscale)Rust-backed 分词 + 流式感知,性能测试的默认选择;(2) NVIDIA GenAI-PerfNVIDIA 参考工具,注意其 ITL 不含 TTFT;(3) LLM-Locust(TrueFoundry)Locust 扩展,修复 GIL 问题;(4) k6 v2026.1.0 + k6 Operador 1.0 GA(2025 年 9 月) Go编译、无 GIL、流式、知感感网-native 分布测试,CI/CD gate 最佳选择──

> **【拓展：CI/CD 中的 SLA Gate】**Em CI usar o SLA gate k6  Configuração: por PR 运行 30-50 次代,gate 指标包括 P50/P95 TTFT、5xx < 5%、TPOT 在值以下──违规规构建失败──使用真实提示分布(mean + stddev of input tokens)而非固定长度LLMPerf 使用`--mean-input-tokens 500 --stddev-input-tokens 150`O que é que é o que é?

**LLMPerf**(Anyscale) Python mas tokenization com Rust. Mean/stddev prompts. Streaming-consciente. Melhor padrão para executar desempenho.

**NVIDIA GenAI-Perf** Referência da NVIDIA. Utiliza o cliente Triton; cobertura métrica abrangente. Observe que sua ITL exclui TTFT; LLMPerf inclui. Duas ferramentas produzem diferentes TPOT para o mesmo servidor.

**LLM-Locust**Extensão de Locus que corrige a armadilha GIL.

**guidellm** Compartilhamento de dados sintéticos em larga escala.

**k6 v2026.1.0**+ **k6 Operator 1.0 GA (Sept 2025)**- Não .
- k6 (Go, compilado, sem GIL) adicionou métricas de streaming.
- k6 O operador utiliza CRDs TestRun / PrivateLoadZone para testes distribuídos nativos Kubernetes.
- Melhor para testes de CI/CD e SLA.

**Vegeta** Vai, mais simples do que k6. Saturação HTTP constante. Não LLM-consciente, mas bom para testes de gateway / limite de taxa.

**Locust 2.43.3 stock** tem a armadilha GIL para LLM. Somente com extensão LLM-Locust.

### Porta SLA em CI

- Executar o PR com:

- 30-50 iterações cada uma no RPS de linha de base.
- Porta: P50/P95 TTFT, 5xx < 5%, TPOT abaixo do limiar.
- - Desligar a construção.

### Distribuição realista de tempo

Construir a partir de amostras reais de tráfego (se você tem) ou de distribuições publicadas (por exemplo, ShareGPT prompts para chat, HumanEval para código).

### Números que você deve lembrar

- k6 Operador 1.0 GA: Setembro 2025.
- K6 v2026.1.0: métricas de streaming conscientes.
- Tópico curso LLMPerf: 100 a 1000 solicitações na simultânea X.
- Portão de CI típico: 30-50 iterações por PR.
- Quatro padrões: constante, rampa, ponta, remoção.

## Use-o com o framework implementado.
```figure
load-pattern-waves
```

## Usá-lo

`code/main.py`Simula um ensaio de carga com uma distribuição realista de velocidade rápida, mede a TPOT eficaz e demonstra a armadilha de velocidade uniforme.

> `code/main.py`Simula um ensaio de carga com uma distribuição realista de velocidade rápida, mede a TPOT eficaz e demonstra a armadilha de velocidade uniforme.

> `code/main.py`Simula um ensaio de carga com uma distribuição realista de velocidade rápida, mede a TPOT eficaz e demonstra a armadilha de velocidade uniforme.

## Envia-o . Produto .

Esta lição produz`outputs/skill-load-test-plan.md`Considerando a carga de trabalho e o SLA, escolhe a ferramenta e desenha os quatro padrões de carga.

> 本课产 出 `outputs/skill-load-test-plan.md`Considerando a carga de trabalho e o SLA, escolhe a ferramenta e desenha os quatro padrões de carga.

## Exercícios.

1. Corra .`code/main.py`Comparar distribuição uniforme vs realista. Onde está a diferença?
   Tradução: 运行`code/main.py`◊ Comparar média vs distribuição real P99 TTFT  Diferença está em onde?
2. Escreva o script k6 para um portão CI: TTFT P95 < 800 ms a 100 concurrent, runtime 5 minutos.
   Tradução do inglês para inglês: C.I. 门控的 k6 脚本:100 并发下 TTFT P95 < 800ms,运行 5 分钟──
3. O teste de remoção mostra que a memória cresce 50 MB/hora.
   O seu teste de absorção mostra que a memória cresce 50MB por hora.
4. Teste de ponta de 10 RPS a 100 RPS. Qual é o tempo de recuperação esperado se a pilha de produção Karpenter + vLLM estiver em funcionamento (fase 17 · 03 + 18)?
   Chinese Translation: de 10 RPS 尖峰测试到100 RPS── Se o Karpenter 需要45秒供应,预期恢复时间是多少?
5. A GenAI-Perf relata TPOT=6ms; LLMPerf relata TPOT=11ms no mesmo servidor.

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| LLMPerf | "the LLM harness" | Anyscale benchmark tool, streaming-aware |
| GenAI-Perf | "NVIDIA tool" | NVIDIA reference harness |
| LLM-Locust | "Locust for LLMs" | Locust extension fixing GIL trap |
| guidellm | "synthetic benchmark" | Large-scale synthetic tool |
| k6 Operator | "K8s k6" | CRD-based distributed k6 |
| GIL trap | "Python client overhead" | Tokenization backlog inflates reported latency |
| Prompt-uniformity trap | "single-prompt lie" | Loop with same prompt hits cache, inflates throughput |
| Steady-state | "constant load" | Flat RPS for N minutes |
| Ramp | "linear up" | 0 to target over duration |
| Spike | "burst test" | Sudden multiplier then revert |
| Soak | "long test" | Hours for leak detection |

## Mais leitura 延伸阅读

- [TianPan — Load Testing LLM Applications](https://tianpan.co/blog/2026-03-19-load-testing-llm-applications)
- [PremAI — Load Testing LLMs 2026](https://blog.premai.io/load-testing-llms-tools-metrics-realistic-traffic-simulation-2026/)
- [NVIDIA NIM — Introduction to LLM Inference Benchmarking](https://docs.nvidia.com/nim/large-language-models/1.0.0/benchmarking.html)
- [TrueFoundry — LLM-Locust](https://www.truefoundry.com/blog/llm-locust-a-tool-for-benchmarking-llm-performance)
- [LLMPerf](https://github.com/ray-project/llmperf)
- [k6 Operator](https://github.com/grafana/k6-operator)
