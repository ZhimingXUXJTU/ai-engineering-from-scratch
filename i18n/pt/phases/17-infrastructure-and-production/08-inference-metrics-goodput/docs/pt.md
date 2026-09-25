# Metricas de inferência  TTFT, TPOT, ITL, Goodput, P99                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

> Quatro métricas determinam se uma implantação de inferência está a funcionar. TTFT é pre-reempimento mais fila mais rede. TPOT (equivalentemente ITL) é o custo de decodificação ligado à memória por token. A latência de ponta a ponta é TTFT mais TPOT vezes comprimento de saída. O rendimento é de tokens por segundo agregados em toda a frota. Mas o que importa para o produto é o goodput  a fracção de pedidos que atenderam a cada SLO simultaneamente. Alta capacidade de produção em baixa potência significa que você está processando tokens que nunca chegam aos usuários a tempo. Números de referência para Llama-3.1-8B-Instruir sobre TRT-LLM em 2026: média TTFT 162 ms, média TPOT 7,33 ms, média E2E 1,093 ms. Sempre relatar P50, P90, P99  nunca apenas mal. E observe a armadilha de medição: a GenAI-Perf exclui o TTFT do cálculo do ITL, a LLMPerf o inclui; duas ferramentas discordam sobre o TPOT para a mesma execução.

> **【中文解读】**Este capítulo apresenta o sistema de indicadores-chave para a qualidade de serviços e a qualidade de gestão de serviços.
**Type:** Learn
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter) | **语言:** Python（标准库，百分位计算器和 Goodput 报告器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 04（vLLM 服务内部）

> - Não .**【前置】**学本节前请先掌握:Fase 17·04(vLLM) 统计基础(百分位) ・・・推理指标四件套:TTFT(首代币 时间) + TPOT(每代币 时间) + 吞吐量 + Goodput。
> - Não .**【类比】**推理指标 = "餐厅 KPI"。TTFT = 顾客坐下第一道菜上桌(prefill+queue+network);TPOT = 后续每道菜间隔(解码成本);吞吐量 = 餐厅每小时出餐总数;Goodput = 满足所有SLO's request proportion(关键!)。陷:高吞吐低 Goodput = fez muitos pratos mas os clientes não conseguiram pagar quando comiam。
**Time:** ~60 minutes | **时间:** ~60 分钟

## Objetivos de aprendizagem

- Defina com precisão o TTFT, o TPOT, o ITL, o E2E, o rendimento e o goodput e nome o componente que cada uma mede.
  中文翻译:精确定义 TTFT、TPOT、ITL、E2E、吞吐量和 Goodput,并说出每个指标测量的组件──
- Explique por que a média é a estatística errada para o serviço de LLM e como ler P50/P90/P99.
  Tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para tradução do inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o inglês para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para o árabe para tradução do árabe para o árabe para o árabe para o árabe para o árabe: p.
- Construa uma restrição múltipla SLO (por exemplo, TTFT < 500 ms E TPOT < 15 ms E E2E < 2 s) e computa o goodput contra ela.
  中文翻译:构造 SLO 多约束(如 TTFT<500ms 且 TPOT<15ms 且 E2E<2s)并据此计算Goodput。
- Cite duas ferramentas de referência que discordam sobre o TPOT para a mesma função e explique o porquê.
  Tradução do inglês para o inglês:                                                                                                                                                                                                                                                          

## O problema é o problema da introdução

> **【中文解读】**推理服务有多个延迟轴,每个轴以不同方式失败──Prefill é computado limitado,随提示长度增长;Decode é内存有限,随批量 增长;排队延迟是运维问题;网络是物理距离问题──needs different indicator to measure each dimension, needs percentage number, also needs a comprehensive indicator to say "user has gotten the expected experience" this is Goodput──

> **【拓展：LLM 推理指标体系】**O sistema de indicadores completos de LLM 推理 comprém: 1) TTFT 首代币 延迟) 用户感知到的首次响应时间; 2) TPOT/ITL() por token 延迟/inter-token 延迟) 流式输出平滑度; 3) E2E(端到端延迟) 从请求到完成的总时间; 4) Throughput(吞吐量) 集群效率指标; 5) Goodput(有效吞吐) 同时满足所有 SLA 请求比例;;ML已经Perf Inference v6.0  Goodput 作为官方提交指标;;

"Nossa capacidade de transferência é de 15.000 tokens por segundo". Então, o que? Se 40% das solicitações passarem por 2 segundos de ponta a ponta, os usuários abandonam a sessão.

> "Nossa capacidade de produção é de 15.000 tokens por segundo"."" Então, como? Se 40% das solicitações de terminação excederem os 2 segundos, o usuário abandonará a conversa"."" Apenas a capacidade de produção não pode dizer-lhe se o produto funciona normal".""

A inferência tem múltiplos eixos de latência e cada um falha de forma diferente. O preenchimento é computacional e as escalas têm um comprimento rápido. O decodificação é baseado na memória e as escalas são do tamanho do lote. O atraso na fila é um problema operacional. A rede é um problema de distância física. Precisamos de métricas distintas para cada uma, e precisamos de percentilhas, e precisamos de um único composto que diga "o usuário obteve o que esperava"

> 推理有多延迟轴,每个轴以不同方式失败──预填是计算有限的,随提示长度增长──解码是内存有限的,随批次大小增长──排队延迟是运维问题──网络是物理距离问题──你需要为每个维度不同的指标,需要百分数,还需要一个综合指标说"用户是否获得预期的体验"这是Goodput──

## O conceito central.

### TTFT  tempo para o primeiro token

> **【中文解读】**TTFT = queue_time + network_request + prefill_time。Prefill 在长提示时占主导32K prompt 在 Llama 3.3 70B FP8 H100 上需要约800ms的纯预填──排队时间是调度器的行为,网络请求包括 TLS 的线缆时间──TTFT 是用户在流式返回任何内容之前感知到的延迟──

`TTFT = queue_time + network_request + prefill_time`

Prefill domina quando os pedidos são longos. No Llama-3.3-70B FP8 no H100, um pedido de 32k leva ~800 ms de prefill puro. O tempo de fila é o comportamento do programador sob carga. A solicitação de rede é o tempo de fio, incluindo TLS. TTFT é a latência que o usuário vê antes de qualquer coisa voltar a fluir.

> 预填充在长提示时占主导──Llama-3.3-70B FP8 在 H100 上,32K 提示需要约800ms的纯预填充──排队时间是负载调度器行为──网络请求是包括 TLS的线缆时间──TTFT是用户在任何内容流式返回前感知到的延迟──

### TPOT / ITL  Latência entre tokens

> **【中文解读】**TPOT(tempo por token de saída) = ITL(latencia inter-token) = latência de decodificação por token。公式:TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced。在 Llama 3.3 70B H100 + 分块预填充下,TPOT 均值约 7ms;无分块预填充时,在长预填 邻居序列期间 TPOT 可升至50ms。永远监控 P99而非均值。

Muitos nomes para uma quantidade.`TPOT`(tempo por token de saída), `ITL`(latencia entre tokens), `decode latency per token`É o tempo entre os tokens transmitidos consecutivos após o primeiro.

> Uma quantidade de nomes.`TPOT`(Per Output token 时间)`ITL`(inter-token 延迟)`每 token 解码延迟`都是同一个──它是第一个标志 之后连续流式标志 间的时间── é o primeiro símbolo 之后连续流式标志 间的时间──

`TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced`

Na mesma pilha Llama-3.3-70B H100 com preenchimento em pedaços, TPOT significa ~ 7 ms. Sem preenchimento em pedaços, durante um longo preenchimento em uma sequência vizinha, TPOT pode aumentar para 50 ms. Observe P99, não significa.

> Durante o mesmo Llama-3.3-70B H100                                                                                                                                                                                                                                                          

### Latência E2E

`E2E = TTFT + TPOT * output_tokens + network_response`

Para saídas longas (> 500 tokens), o E2E é dominado pela TPOT. Para saídas curtas com pedidos longos, o E2E é dominado pela TTFT. Relata o E2E condicionado pela extensão da saída.

> 对于长输出(>500 tokens),E2E por TPOT 主导──对长提示的短输出,E2E por TTFT 主导──报告按输出长度分条件的E2E──

### Transmissão

`throughput = total_output_tokens / elapsed_time`

A métrica agregada diz-te a eficiência da frota, não a saúde individual.

> 聚合指标――告诉你集群效率――不告诉你单单请求的健康状况―― não diz-te o estado de saúde de uma única solicitação――

### O que é que você realmente quer saber?

> **【中文解读】**O Goodput é o único indicador integral realmente importante. O SLO é um requisito de muito volume. Um pedido só pode ser feito simultaneamente para satisfazer o TTFT <= a、TPOT <= b、E2E <= c 才算"好"── Alto consumo em 60% O Goodput 时是失败; baixo consumo em 99% O Goodput 时才是目标──2026 anos MLPerf Inference v6.0 和 AI 平台供应商内部 SLA 追踪都以 Goodput为核心指标──

`goodput = fraction of requests meeting (TTFT <= a) AND (TPOT <= b) AND (E2E <= c)`

O SLO é uma restrição múltipla. Um pedido é "bom" apenas se cada restrição for cumprida. Goodput é a participação.

> O SLO é de muitos limites. Apenas quando todos os limites são satisfeitos, o pedido é "bom". O Goodput é essa parte.

Em 2026, o goodput é a métrica usada nas submissões MLPerf Inference v6.0 e no rastreamento interno de SLA nos provedores de plataforma de IA.

> 2026 年,Goodput 是 MLPerf Inference v6.0 提交和 AI 平台提供商内部 SLA 追踪使用的指标──

### Por que a média é a estatística errada

> **【中文解读】**LLM 延迟分布是右偏的──一个包含长预填 邻居的解码批可能发发发 500 个 TPOT ~7ms的代币 和 20 个 TPOT ~60ms 的代币──平均值 TPOT 是 9ms,但 P99 TPOT 是 65ms──用户经常遇到 P99这是他们离开的原因──永远报告三元组(P50, P90, P99),对于用户体验,P99是需要优化的目标──

As distribuições de latência LLM são distorcidas à direita. Um lote de decodificação com um vizinho de pre-preenchimento longo pode enviar 500 tokens com TPOT ~ 7 ms e 20 tokens com TPOT ~ 60 ms.

> LLM 延迟分布是右偏的──一个包含长预填充邻居的解码批次可以发发发 500 个 TPOT 约7ms的代币和 20 个 TPOT 约60ms的代币──平均值 TPOT 是 9ms──P99 TPOT 是 65ms──用户经常遇到 P99这就是他们离开的原因──

Sempre informe o triplo (P50, P90, P99). Para a experiência do usuário, P99 é o que você otimiza.

> 始终报告三元组(P50、P90、P99)。 Para a experiência do usuário, P99 é o que você precisa melhorar。

### Números de referência  Llama-3.1-8B-Instrução sobre TRT-LLM, 2026

- TTFT médio: 162 ms
  中文翻译:均值 TTFT:162ms
- TPOT médio: 7,33 ms
  中文翻译:均值 TPOT:7.33ms
- média E2E: 1.093 ms
  中文翻译:均值 E2E:1,093ms
- P99 TPOT: varia entre 10 e 25 ms, dependendo da configuração de preenchimento em pedaços.
  Chinese:P99 TPOT:10-25ms,取决于分块预填配置──

Estes são os pontos de referência publicados da NVIDIA. Eles mudam com o tamanho do modelo (70B mostraria 3-5x), hardware (H100 vs. B200 ~ 3x), e carga.

> Estes são dados de referência publicados pela NVIDIA. Eles são comparados com o modelo.

### A armadilha de medição

> **【中文解读】**Os dois instrumentos de teste de base mais comuns em 2026 em TPOT produzem resultados diferentes: NVIDIA GenAI-Perf vai excluir TTFT do ITL  cálculo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

> **【拓展：LLM 基准测试工具生态】**2026 ano LLM 推理基准测试工具包括:(1) NVIDIA GenAI-PerfTriton 客户端,全面指标覆盖,ITL 不含TTFT;(2) LLMPerf(Anyscale)Rust-backed 分词,流式感知,含TTFT的ITL;(3) LLM-Locust(TrueFoundry)Locust 扩展,修复 GIL 问题;4) guidelm大规模合成基准测试;5)((((k6 v2026.1.0流式感知,Kubernetes-native──选择工具时要了解其ITL 定义差异──

Duas das ferramentas de referência mais utilizadas para 2026 discordam sobre o TPOT para a mesma execução:

- **NVIDIA GenAI-Perf**O ITL começa com o token 2.
  Tradução:**NVIDIA GenAI-Perf**: de ITL 计算中排除 TTFT──ITL de 第 2 个代币 开始──
- **LLMPerf**O ITL começa com o token 1.
  Tradução:**LLMPerf**O TTFT foi incluído em 1o token.

Para uma solicitação com TTFT 500 ms e 100 tokens de saída em 700 ms total de decodificação, GenAI-Perf relata `ITL = 700/99 = 7.07 ms`, relatórios da LLMPerf `ITL = 1200/100 = 12.00 ms`A escolha da ferramenta muda o número.

>  Para um TTFT 500ms  100  saída de token  700ms  total de resolução de pedido, GenAI-Perf  relatório `ITL = 700/99 = 7.07ms`,LLMPerf  relatório `ITL = 1200/100 = 12.00ms`❖ ferramentas para mudar o número.

Sempre indicar qual ferramenta.

> 始终说明使用哪个工具──始终发布定义──

### Construção de um SLO

> **【拓展：LLM SLO 设定参考】**2026 ano de recomendação de consumo classe 70B 对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 token 输出)、Goodput >= 99%。企业级 SLO 收紧 TTFT(200-400ms)`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`), objetivo 2x 峰值并发,运行 30-50 次代取百分位数──

Um SLO razoável para o consumidor para um modelo de chat 70B em 2026:

- TTFT P99 <= 800 ms.
  中文翻译:TTFT P99 <= 800ms(首代币 延迟上限)
- TPOT P99 <= 25 ms.
  中文翻译:TPOT P99 <= 25ms(per token 延迟上限)
- E2E P99 <= 3 s para saídas de < 300 tokens.
  中文翻译:E2E P99 <= 3s(<300 token 输出) 』
- Objetivo de produção de energia >= 99%.
  中文翻译:Goodput 目标 >= 99%。

Os SLOs Enterprise apertam o TTFT (200-400 ms) e afrouxam o E2E. O ponto é anotá-los, medir os três e rastrear o goodput como um único composto.

> 企业级 SLO 收紧 TTFT(200-400ms)并放宽 E2E──关键是要写下来、测量全部三、并将Goodput 作为单一综合指标追踪──

### Como medir

- Execução de tráfego real ou realista sintético (LLMPerf com `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`)).
  Tradução do inglês:运行真实流量或逼真合成流量`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`)。
- Objectivo 2x de simultaneidade máxima para a corrida de referência.
  O objetivo do teste de base é 2 vezes o valor de pico.
- Execute 30 a 50 iterações, pegue percentilhas da amostra combinada.
  Tradução do inglês:运行 30-50 次代,取合并样本的百分位数──
- Publicação com nome da ferramenta, versão da ferramenta, modelo, hardware, concurência, distribuição rápida.
  Chinese: 發布時标注 工具名,版本,模型,硬件,并发数,提示,分布,

## Use-o com o framework implementado.
```figure
throughput-latency
```

## Usá-lo

`code/main.py`É uma calculadora de bom desempenho de brinquedo. Gerar uma distribuição de latência sintética, aplicar um SLO e calcular o bom desempenho. Também mostra a diferença GenAI-Perf vs LLMPerf TPOT no mesmo rastro.

> `code/main.py`É um modelo de Goodput  calculador。 produzir síntese de diferença de diferença de diferença de tempo, aplicando SLO, calcular Goodput。 também mostrando o mesmo rastro 上 GenAI-Perf vs LLMPerf  TPOT 差异。

## Envia-o . Produto .

> **【拓展：SLO 设定与 Goodput 门控】**O modelo de 70B para o ano de 2026 foi recomendado SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 tokens 输出)、Goodput 目标 >= 99%。 SLO 收紧 TTFT(200-400ms) mas amplo E2E──关键实践:(1) Em um CI/CD central gate 部署决策于 Goodput value而非吞吐量;(2) 用 2x 峰并发行基准测试;((((运行 30-50 次取百分位数;(4) 发布时标标工具名、版本、模型、硬件、发发数、代提示分布;;

Esta lição produz`outputs/skill-slo-goodput-gate.md`- Tendo em conta a carga de trabalho e o SLO, produz uma receita de referência preta para a CI/CD que os portões utilizam em vez de emissão.

> 本课产 出 `outputs/skill-slo-goodput-gate.md` Dado o trabalho de carga e SLO, ele gera um CI/CD em seu nível de teste de base, com Goodput e não de produção como controle de implantação.

## Exercícios.

1. Corra .`code/main.py`Como o goodput muda quando tens P99 TPOT de 30 ms para 15 ms?
   Tradução: 运行`code/main.py` gerar com 1% de distribuição de ponta.  Quando P99 TPOT de 30ms 收紧到15ms 时 Goodput 如何变化?
2. Um vendedor cita "15.000 tok/s em Llama 3.3 70B H100". Cite três perguntas a fazer antes de confiar nele.
   Tradução do inglês para "Llama 3.3 70B H100 上 15,000 tok/s"
3. Por que o preenchimento em pedaços protege o P99 TPOT mas não o TPOT?
   Por que é que o P99 TPOT não é um TPOT de valor médio?
4. Construa um SLO de consumo para um assistente de voz (o primeiro token é ouvido, não lido). Qual métrica é mais visível ao usuário?
   Chinese Language Translation: 為语音助手构建消费级 SLO(首代令是听到而非读到) ―― qual é o indicador mais visível para o usuário?
5. Leia o documento LLMPerf README e o documento GenAI-Perf. Identifique outras três métricas em que as ferramentas discordam.
   Tradução do inglês para tradução do inglês:

## Termos-chave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| TTFT | "time to first token" / "首 token 时间" | Queue + network + prefill; dominated by prefill at long prompts / 队列+网络+预填充；长提示时由预填充主导 |
| TPOT | "time per output token" / "每输出 token 时间" | Memory-bound decode cost per token after first / 首个 token 后每 token 的内存受限解码成本 |
| ITL | "inter-token latency" / "inter-token 延迟" | Same as TPOT in most tools (not all — see GenAI-Perf) / 大多数工具中同 TPOT（非所有——见 GenAI-Perf） |
| E2E | "end to end" / "端到端" | TTFT + TPOT * output_len; response-side network on top / TTFT + TPOT * 输出长度；加上响应端网络 |
| Throughput | "tok/s" / "token 每秒" | Fleet efficiency; useless without latency percentiles / 集群效率；无延迟百分位数则无意义 |
| Goodput | "SLO-met rate" / "SLO 达标率" | Fraction of requests meeting every SLO constraint simultaneously / 同时满足所有 SLO 约束的请求比例 |
| P99 | "tail" / "尾部" | 1-in-100 worst-case latency; the user experience metric / 百分之一最差延迟；用户体验指标 |
| SLO multi-constraint | "the joint" / "联合约束" | AND of all three latency bounds; a request fails if any one is violated / 三个延迟界限的 AND；任一违反即失败 |
| GenAI-Perf vs LLMPerf | "the tool trap" / "工具陷阱" | Tools disagree on whether ITL includes TTFT / 工具在 ITL 是否包含 TTFT 上不一致 |

## Mais leitura 延伸阅读

- [NVIDIA NIM — LLM Benchmarking Metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html) definição canónica do TTFT, ITL, TPOT.
- [Anyscale — LLM Serving Benchmarking Metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics) definições alternativas e receita de medição.
- [BentoML — LLM Inference Metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics) medição aplicada em implantações reais.
- [LLMPerf](https://github.com/ray-project/llmperf) Referência de código aberto baseada em raios.
- [GenAI-Perf](https://github.com/triton-inference-server/perf_analyzer/blob/main/genai-perf/README.md) Ferramenta de referência da NVIDIA.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) o índice de referência baseado em bons resultados aceito pela indústria.
