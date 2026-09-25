# TensorRT-LLM em Blackwell com FP8 e NVFP4
# Compilação de Inferência Especializada em Hardware  FP8 e NVFP4 em Blackwell

> Compilação de inferências especializada em hardware negocia portabilidade para o throughput, e TensorRT-LLM  NVIDIA-só, sintonizado para Blackwell  é o exemplo mais claro do comércio dando frutos.$0.012 per million tokens on a 120B model in Q1-Q2 2026, against $0,09/M em H100 + vLLM  uma diferença económica de 7x. A pilha é composta por três regimes de pontos flutuantes: FP8 permanece crítico para cache KV e núcleos de atenção porque tem a faixa dinâmica que eles precisam; NVFP4 (4-bit microscaling) lida com pesos e ativações; previsão multi-token (MTP) e prefill / decode desagregado adicionar mais 2-3x no topo. O modelo de suporte Day-0 carrega pesos FP4 diretamente sem conversão pós-treino. A atração para as equipes de engenharia de 2026: TRT-LLM é open source, mas específica para NVIDIA  CUDA- e Blackwell especializada , então adotando-a negocia com a portabilidade para a capacidade de transmissão. Faça as contas com a sua mistura de modelos e hardware antes de se comprometer.

> **【中文解读】**Este capítulo apresenta o TensorRT-LLM e o BlackwellNVIDIA LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
**Type:** Learn
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 13 (Quantization)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator) | **语言:** Python（标准库，FP8/NVFP4 内存和成本计算器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 13 (Quantization) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 13（量化）

> - Não .**【前置】**O TensorRT-LLM é NVIDIA 专属优化, em Blackwell GPU 上性能最强
> - Não .**【类比】**TensorRT-LLM = "NVIDIA 专属跑车"―GB200 NVL72 上 SemiAnalysis 测:120B 模型 $0.012/百万 token（H100+vLLM $0.09)  7 倍 经济性差距──三套浮点叠加:FP8(KV cache+attention 动态范围) + NVFP4(4-bit 权重激活) + MTP/解 prefill-decode 再加 2-3 倍──代价:闭源 NVIDIA ,可移植性换吞吐──选型前必须按你的模型/硬件组合算账──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Objetivos de aprendizagem

- Explique por que o FP8 permanece crítico para o cache e a atenção do KV mesmo quando os pesos estão no NVFP4.
  Tradução do inglês para o inglês: Explain why even weight in NVFP4, FP8 for KV 缓存和注意力仍然关键──
- Calcular a pegada HBM de um modelo de fronteira sob o BF16, FP8 e NVFP4 e explicar de onde vêm as economias.
  O modelo de cálculo da linha de frente em BF16、FP8 e NVFP4 占用,分析节省来自哪里──
- Nomear as características específicas do Blackwell que utilizam o TRT-LLM (dia-0 FP4, MTP, serviço desagregado, primitivos para todos).
  Tradução do português em português: 说出 TRT-LLM利用的黑威尔特有功能(day-0 FP4、MTP、分离式服务、all-to-all 原语)。
- Decida quando o bloqueio NVIDIA da TRT-LLM vale a diferença de custo 7x contra o vLLM no Hopper.
  Chinese: decide TRT-LLM's NVIDIA 锁定何时值相比Hopper 上 vLLM's 7x 成本差距──

## O problema é o problema da introdução

> **【中文解读】**2026 ano de teoria econômica da linha de frente é "cada dólar quanto token"── a resposta depende de quatro níveis de superposição: hardware代际: Hopper H100/H200 vs Blackwell B200/GB200) 、精度(BF16 → FP8 → NVFP4)、 teoria do motor(vLLM vs SGLang vs TRT-LLM)$0.09/M tokens；在 Blackwell + TRT-LLM + Dynamo 上仅 $O preço da diferença é NVIDIA Lockdown, que não pode ser reproduzido em hardware de outros fabricantes.

> **【拓展：NVIDIA Blackwell 架构】**Blackwell(B200/GB200) é uma GPU arquitectura lançada pela NVIDIA 2024-2025 anos, em comparação com Hopper (H100) em LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       

A fronteira da economia de inferência em 2026 é "quantos tokens por dólar". A resposta depende de quatro escolhas empilhadas: geração de hardware (Hopper H100/H200 vs Blackwell B200/GB200), precisão (BF16 → FP8 → NVFP4), motor de servidão (vLLM vs SGLang vs TRT-LLM), e orquestração (plain vs disaggregated vs Dynamo).

> 2026 ano de teoria econômica é "cada dólar quanto token"── resposta depende de quatro superposição seleção: hardware代际(Hopper vs Blackwell)、精度(BF16 → FP8 → NVFP4)、 teoria motor(vLLM vs SGLang vs TRT-LLM)

No Hopper com VLLM, um MoE 120B corre em ~$0.09 per million tokens. On Blackwell with TRT-LLM + Dynamo, the same model runs at ~$A diferença entre o hardware e o hardware é de 11 a 15x por GPU LLM em relação ao Hopper.

> Em Hopper + VLLM 上,120B MoE 运行约 $0.09/M tokens。在 Blackwell + TRT-LLM + Dynamo 上，同一模型运行约 $0.012便宜 7 倍──部分差距来自硬件(Blackwell vs Hopper Cada GPU LLM 吞吐 11-15 倍)──部分来自:FP4 权重、MTP draft、分离式预填充/解码和 NVLink 5 all-to-all Used for MoE 专家通信──

Não se pode replicar isso fora da pilha da NVIDIA. Isso é a troca  portabilidade para a economia. Entender quais opções da pilha dão qual parte da lacuna é o ponto desta lição.

> Você não pode reproduzir fora da NVIDIA. É o que significa que a economia é transformada.

## O conceito central.

### Por que o FP8 ainda é o piso para o cache KV

> **【中文解读】**FP8 é o requisito de precisão mínima do KV Cache. O KV Cache  armazenamento                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

Um erro comum em 2026: assumir que NVFP4 se aplica em todos os lugares. Não. O cache KV precisa de FP8 (8 bits flutuantes) porque armazena chaves de atenção e valores que abrangem uma ampla faixa dinâmica. Quantizar KV para FP4 causa perda de precisão catastrófica  a cauda da distribuição cai e as pontuações de atenção colapsam.

> Um erro comum de 2026: supõe que NVFP4  se aplica a todas as regiões. Não é de. KV 缓存需要FP8;; 8位浮点), pois o seu armazenamento atravessa um amplo espectro de atividades.

NVFP4 (2025-2026) aplica-se a pesos e ativações. Microscaling: cada bloco de pesos tem seu próprio fator de escala para que pequenos blocos possam abranger diferentes intervalos dinâmicos sem perda de escala por tensor. Para ativações, FP4 mantém-se porque as ativações são de pequeno alcance dentro de uma camada.

> NVFP4 ((2025-2026) aplica-se ao peso e à atividade. Micronização: cada bloco de peso tem seu próprio fator de contração, o bloco pode atravessar diferentes níveis de movimento sem perder a quantidade de contração.

A configuração típica de Blackwell:

- Pesos: NVFP4 (4 bits de microscálise).
  中文翻译:权重:NVFP4(4-bit 微缩放) 』
- Ativações: NVFP4.
  Tradução do português:激活:NVFP4──
- Caché KV: FP8.
  O que é o "Caso de Resistência"
- Acumulador de atenção: FP32 (estabilidade de suavidade máxima).
  Tradução do inglês:

### Os primitivos específicos de Blackwell utilizam TRT-LLM

- **Day-0 FP4 weights**A Comissão propõe que os modelos de transporte de carga sejam utilizados para a realização de uma avaliação de qualidade e de qualidade de qualidade.
  Tradução:**Day-0 FP4 权重**O modelo fornecedor de FP4 权重;TRT-LLM 无需训练后转换即可载;;FP4 不需要 AWQ/GPTQ 步骤;;
- **Multi-token prediction (MTP)**A proposta de directiva é a seguinte:
  Tradução:**多 token 预测 (MTP)**A fase 17 · 05), mas integrada ao TRT-LLM 构建中──
- **Disaggregated serving**A ideia é a mesma que a Dynamo (Fase 17 · 20).
  Tradução:**分离式服务**Pre-fill e code em GPU independente, KV 缓存通过NVLink ou InfiniBand 传输──
- **All-to-all communication primitives**A NVLink 5 reduziu a latência de comunicação de especialistas em MoE em 3x contra Hopper.
  Tradução:**All-to-all 通信原语**A NVLink 5 vai reduzir o tempo de comunicação de 3 vezes.
- **NVFP4 + MXFP8 microscaling**A manipulação acelerada de fatores de escala em núcleos tensores Blackwell.
  Tradução:**NVFP4 + MXFP8 微缩放**O Blackwell Tensor Core acima do hardware aceleração de processamento de fatores de envelhecimento.

### Os números que você deve memorizar

- HGX B200 a US$ 0,02 / M em tokens GPT-OSS-120B via TRT-LLM.
  Chinese: HGX B200 , em GPT-OSS-120B , em TRT-LLM , em tokens de US $ 0,02 / M .
- GB200 NVL72 a tokens de US$ 0,012/M via Dynamo (orquestração TRT-LLM).
  O banco central da China (BTC) está em negociações com o Banco Central do Brasil.
- H100 + vLLM ≈ $ 0,09 / M tokens em carga de trabalho comparável.
  Chinese: H100 + vLLM 在可比工作负载上约$0,09 /M tokens──
- Aumento de 2,8 vezes em três meses de atualizações do TRT-LLM (2026).
  Tradução do inglês:TRT-LLM 2026
- 11-15 vezes por GPU LLM de rendimento, Blackwell vs Hopper.
  Tradução do inglês: Blackwell vs Hopper
- MLPerf Inference v6.0 (abril 2026): Blackwell domina todas as tarefas submetidas.
  Inferência M.L.Perf v6.0(2026 年 4 月):Blackwell 在所有提交任务中领先──

### Quanto custa a qualidade do FP4

> **【中文解读】**A NVFP4 em raciocínio intensivo de trabalho ([[思维链]], [[mathematics]],长上下文代码生成]]) pode levar a uma degradação de qualidade visível. Cada bloco de classificação pode ser aliviado, mas não pode ser eliminado.

> **【拓展：量化精度 vs 推理成本权衡】**A seleção da precisão quantitativa é o peso da qualidade e do custo: 1) BF16 não tem perda de qualidade, mas a demanda de memória é grande; 2) FP8 quase não tem perda; 3) INT4AWQ/GPTQ) 4-bit  peso, MATH 分数下降 3-5点,适合通用聊天; 4) NVFP4最激进, Blackwell 专用,必须在目标评估上精准.

NVFP4 é agressivo. Em cargas de trabalho pesadas de raciocínio (cadeia de pensamento, matemática, código-gen com longo contexto), os pesos FP4 se degradam visiblemente. A calibração por bloco mitiga, mas não elimina. Os modelos de raciocínio de equipes geralmente usam pesos FP8 + ativações FP4 como um compromisso, ou se apegam ao H200 com FP8 em todo.

> NVFP4 é ativado. Em funções de cálculo intenso tipo de trabalho ([[pensamento]], matemática]], desenvolvimento de código de código) em,FP4 é ativado.

A regra: sempre valida a qualidade da tarefa no seu conjunto de avaliação antes de se comprometer com pesos NVFP4.

> 规则: 始终在您的评估集上验证任务质量. 

### Por que é uma decisão de bloqueio da NVIDIA

> **【中文解读】**TRT-LLM é um conjunto de C++ + CUDA + 闭源内核的组合──模型需要为特定 GPU SKU 编译──不支持 AMD、Intel 或 ARM──如果你的基础设施策略是多供应商,TRT-LLM 对于这个层是不可选项你仍然可以在混合硬件上使用vLLM──但如果你是NVIDIA-only,7x的经济差值得这个锁──

> **【拓展：NVIDIA vs AMD 推理生态】**2026  AI  Raciocínio do mercado de chips: NVIDIA  Com CUDA 生态 e TRT-LLM  ocupando cerca de 80% da quota de raciocínio de data center.

TRT-LLM é um kernel de código fechado. Os modelos precisam ser compilados para um SKU específico de GPU. Sem AMD, sem Intel, sem ARM. Se sua estratégia infra é multi-vendor, TRT-LLM é um não-starter para o nível TRT-LLM servido.

> TRT-LLM é um conjunto de C++ + CUDA + 闭源内核的组合――模型需要为特定 GPU SKU 编译――不支持 AMD、Intel 或 ARM――如果你的基础设施策略是多供应商,TRT-LLM不可行你仍然可以在混合硬件上使用vLLM――如果你是NVIDIA-only,7x 差距值得这个锁──

### 2026 receita prática

Para uma conta de inferência anual de US$ 100 milhões, executar Hopper + vLLM deixa 7-10x na mesa. Migração de cargas de trabalho dominantes de custo para Blackwell + TRT-LLM + Dynamo. Mantenha o nível de experimentação em H100 + vLLM para a velocidade de iteração do modelo. Valida a qualidade em cada modelo convertido NVFP4 antes da produção.

>  Para o gasto anual de US$ 100 milhões +, a operação no Hopper + vLLM significa deixar 7-10 vezes o espaço de poupança

### O bônus de desagregação

A porção desagregada do TRT-LLM (pools separados de preenchimento e decodificação) é coberta em profundidade na fase 17 · 20. Na Blackwell, os multiplicadores são empilhados: pesos FP4 × aceleração MTP × colocação desagregada × roteamento consciente de cache. O número 7x assume esta pilha completa.

> TRT-LLM's separação de serviços ([[Independent Prefill and Settlement Pool]]) em Fase 17 · 20 中深入讨论──在Blackwell 上,乘数叠加:FP4 权重 × MTP 加速 × 分离式部署 × 缓存感知路由──7x 数字假设使用完整──

## Use-o com o framework implementado.

> **【拓展：Blackwell 迁移决策】**Desde Hopper 迁移到Blackwell + TRT-LLM 决策框架:(1) 推理支出是否超过5M$?是→值得评估迁移;(2) 是否可以接受NVIDIA 锁定?否→继续使用vLLM + Hopper;(3) 工作负载是否包含MoE 模型?是→Blackwell NVLink 5 all-to-all 提供额外3x 加速;(4) 推理密集型任务占成是否超过30%?是→需要验证 NVFP4 质量──迁移 ROI通常在 6-12 个月内回本.
```figure
pipeline-parallel
```

## Usá-lo

`code/main.py`calcula a pegada HBM, o decodificador de throughput (regime de memória limitada) e os tokens $/M para um modelo em três pilhas: H100 + BF16 + vLLM, H100 + FP8 + vLLM, B200 + NVFP4/FP8 + TRT-LLM. Execute-o para ver o efeito de composição e a proporção da lacuna que cada mudança contribui.

> `code/main.py`計算模型在三上 HBM 占用、解码吞吐量(内存受限) 和 $/M-tokens:H100 + BF16 + vLLM、H100 + FP8 + vLLM、B200 + NVFP4/FP8 + TRT-LLM──运行它查看复合效应和每个变化贡献差距份额──

## Envia-o . Produto .

Esta lição produz`outputs/skill-trtllm-blackwell-advisor.md`. Dada a carga de trabalho, o tamanho do modelo e o volume anual dos tokens, decide se a pilha Blackwell + TRT-LLM vale a pena o bloqueio NVIDIA.

> 本课产 出 `outputs/skill-trtllm-blackwell-advisor.md` Dado o volume de tokens anuais, o Blackwell + TRT-LLM  vale a pena ser bloqueado pela NVIDIA 

## Exercícios.

1. Corra .`code/main.py`Em um MoE 120B com parâmetros ativos de 30%, calcular o rendimento de decodificação limitada de largura de banda de memória em H100 BF16, H100 FP8 e B200 NVFP4/FP8.
   Tradução: 运行`code/main.py` Em 30%                                                                                                                                                                                                                                                             
2. Um cliente gasta US$ 2 milhões por ano em H100 + vLLM. Qual é o número de GPUs Blackwell que eles precisam comprar para amortizar uma migração para TRT-LLM em 12 meses, dada a lacuna econômica de 7x?
   Chinese Translation: clientes em H100 + vLLM 上每年花费2M.
3. Você vê a queda de precisão 3 pontos no MATH após a conversão de peso NVFP4. Nomear dois caminhos de recuperação: um de qualidade em primeiro lugar (manter pesos FP8) e um de custo em primeiro lugar (calibrar com dados no domínio).
   Chinese Language Translation:NVFP4 权重转换后 MATH 精度下降 3 点──说出两条恢复路径:一条质量优先(保持 FP8 权重),一条成本优先(用领域内数据校准)
4. Leia os resultados da inferência do MLPerf v6.0. Qual tarefa tem a menor lacuna de Blackwell-over-Hopper e porquê?
   Chinese: 阅读 MLPerf v6.0 推理结果──哪个任务的黑威尔-over-Hopper 差距最小,为什么?
5. Compute o HBM necessário para um modelo 405B com pesos NVFP4 + FP8 KV cache em contexto 128k.
   Chinese:计算 405B 模型在 NVFP4 权重 + FP8 KV 缓存 + 128k 上下文下 HBM 需求──它是否适合单个GB200 NVL72 节点?

## Termos-chave .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| FP8 | "eight-bit float" / "8-bit 浮点" | 8-bit floating point; used for KV cache and attention due to dynamic range / 8-bit 浮点；因动态范围用于 KV 缓存和注意力 |
| NVFP4 | "four-bit micro" / "4-bit 微缩放" | NVIDIA's 4-bit microscaling FP format; weights and activations on Blackwell / NVIDIA 4-bit 微缩放浮点格式；Blackwell 上的权重和激活 |
| MXFP8 | "MX eight" / "MX 8-bit" | Microscaling FP8 variant; hardware-accelerated on Blackwell Tensor Cores / 微缩放 FP8 变体；Blackwell Tensor Core 硬件加速 |
| Day-0 FP4 | "ship FP4 weights" / "直接发布 FP4 权重" | Model providers release weights already in FP4; no post-train conversion step / 模型提供商直接发布 FP4 权重；无训练后转换步骤 |
| MTP | "multi-token prediction" / "多 token 预测" | TRT-LLM's integrated speculative-decoding draft (Phase 17 · 05) / TRT-LLM 集成的推测解码 draft |
| Disaggregated serving | "split prefill/decode" / "分离预填充/解码" | Prefill and decode on separate GPU pools; KV transferred over NVLink/IB / 独立 GPU 池的预填充和解码 |
| All-to-all | "MoE expert comm" / "MoE 专家通信" | Communication pattern routing tokens to expert GPUs; NVLink 5 cuts 3x / 将 token 路由到专家 GPU 的通信模式 |
| InferenceX | "SemiAnalysis inference bench" / "推理基准" | The 2026 industry-accepted cost-per-token benchmark / 2026 年行业接受的每 token 成本基准 |

## Mais leitura 延伸阅读

- [NVIDIA — Blackwell Ultra MLPerf Inference v6.0](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/) Abril 2026 Resultados do MLPerf.
- [NVIDIA — MoE Inference on Blackwell](https://developer.nvidia.com/blog/delivering-massive-performance-leaps-for-mixture-of-experts-inference-on-nvidia-blackwell/)- NVLink 5 todos-a-todos e núcleos MoE.
- [TensorRT-LLM Overview](https://nvidia.github.io/TensorRT-LLM/overview.html) documentação oficial do motor.
- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/) Orquestração desagregada acima da TRT-LLM.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) o conjunto de referências que publica números Blackwell.
