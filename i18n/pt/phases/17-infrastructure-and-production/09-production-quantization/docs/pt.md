# Quantização da produção  AWQ, GPTQ, GGUF K-quants, FP8, MXFP4/NVFP4                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

> O formato de quantização não é uma escolha universal  é uma função de hardware, motor de serviço e carga de trabalho. O GGUF Q4_K_M ou Q5_K_M possui CPU e Edge, entregues através de llama.cpp e Ollama. O GPTQ ganha dentro do VLLM quando você precisa de multi-LoRA na mesma base. AWQ com kernels Marlin-AWQ entrega ~741 tok/s em um modelo de classe 7B com o melhor Pass@1 em INT4  o padrão 2026 para produção de datacenter. FP8 permanece no meio de Hopper, Ada e Blackwell  quase sem perdas e amplamente apoiado. NVFP4 e MXFP4 (microscaling Blackwell) são agressivos e exigem validação por bloco. Duas equipes de armadilhas: o conjunto de dados de calibração deve corresponder ao domínio de implantação, e o cache KV é separado da quantização de peso  a lição AWQ "meu modelo é 4 GB agora" esquece o cache KV de 10-30 GB em tamanhos de lote de produção.

> **【中文解读】**Esta secção apresenta a aplicação da tecnologia de quantificação de produção ambiental da INT8/INT4/FP8 na redução dos custos de cálculo.
**Type:** Learn
**Languages:** Python (stdlib, toy memory and throughput comparison across formats)
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy memory and throughput comparison across formats) | **语言:** Python
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals)

> - Não .**【前置】**學本节前 請先掌握:Fase 10·13(量化基础) ‧Fase 17·04(vLLM) ‧量化格式不是普适选择按硬件+引擎+工作负载选──
> - Não .**【类比】**量化格式 = "压缩行李"。GGUF Q4_K_M = 适合火车/edge(CPU 友好);GPTQ = vLLM 多 LoRA 场景;AWQ + Marlin 内核 = 数据中心默认(7B 模型 741 tok/s,INT4 最佳);FP8 = Hopper/Ada/Blackwell 中选择(近乎无损);NVFP4/MXFP4 = 激进,需块逐验证。
> ️ **【易错点】**两个陷:(1) 校准数据集必须匹配部署领域(医疗模型用通用文本校准会失真);(2) "Meu modelo é apenas de 4GB" 忘了KV cache(production batch 下 10-30GB)。
**Time:** ~75 minutes | **时间:** ~75 minutes

## Objetivos de aprendizagem

- Nomear os seis formatos de quantização da produção e os seus pontos de sucesso em 2026.
  Chinese:                                                                                                                                                                                                                                                              
- Escolha um formato dado ao hardware (CPU vs GPU, Hopper vs Blackwell), motor (vLLM, TRT-LLM, llama.cpp), e carga de trabalho (chat de rotina, raciocínio, multi-LoRA).
  Segundo o texto, o sistema operacional foi criado para o uso de computadores de computadores de computador.
- Calcule a memória de peso salvada e o cache KV deixado intocado para um formato escolhido.
  O que é o "Caso de Reserva" de um Estado?
- Nomear a armadilha do conjunto de dados de calibração que degrada os modelos quantizados no tráfego de domínio.
  Tradução do inglês para o inglês:

## O problema é o problema da introdução

> **【中文解读】**Quantização reduzida de memória e HBM 带宽消耗正是最需要的阶段. FP16 型号重量占用140GB,INT4 量化后仅35GB,可运行在一张H100上. 80GB HBM) 但量化不是免费激进的量化降低质量.                                                                                                                                                                                                                    

> **【拓展：量化技术演进】** 量化技术经历了三代:(1) 均量化(INT8/INT4)  简单但精度损失大;(2) 感知量化(AWQ/GPTQ)  保护重权重要,INT4 下质量接近BF16;(3) 浮点量化(FP8/NVFP4) 硬件加速,动态范围更好──2024-2026  量化研究的核心突破是"微缩放"(microscaling)  权力块有独立缩放因子,在4-bit下仍然保持良好──ARK Invest 估计量化贡献了推成本下降约30%──

A quantização reduz a memória e a largura de banda HBM, que é exatamente o que a decodificação precisa. Um modelo FP16 70B é de 140 GB de pesos. Quantize pesos para INT4 (AWQ ou GPTQ) e o modelo é de 35 GB  cabe em um H100 com espaço para cache KV, o que importa porque em 128 sequências simultâneas com contexto 2k, o cache KV sozinho é de 20-30 GB.

> Quantização reduzida de memória e HBM 带宽消耗, é o que mais se precisa.  FP16  70B 模型权重占140GB.   权重将重量化为INT4 AWQ或GPTQ) 后模型只能在一张H100 上运行,还有空间放 KV 缓存,这在128 并发序列、2K 上下文时很重要,因为 KV 缓存单独需要 20-30GB.

Mas a quantização não é gratuita. A quantização agressiva degrada a qualidade, especialmente em tarefas pesadas de raciocínio. Diferentes formatos funcionam com diferentes motores. Diferentes hardware suportam diferentes precisões nativamente. O formato zoológico 2026 é real e você não pode copiar a escolha de outra pessoa.

> Mas a quantificação não é gratuita. A quantificação intensificada reduz a qualidade, especialmente em função de tarefas de tipo intenso. Diferentes formatos de equipamento são utilizados em diferentes motores. Diferentes hardware nativos são utilizados em diferentes precisões.

## O conceito central.

### Os seis formatos

| Format | Bits | Sweet spot | Engines |
|--------|------|-----------|---------|
| GGUF Q4_K_M / Q5_K_M | 4-5 | CPU, edge, laptops | llama.cpp, Ollama |
| GPTQ | 4-8 | Multi-LoRA on vLLM | vLLM, TGI |
| AWQ | 4 | Datacenter GPU production | vLLM (Marlin-AWQ), TGI |
| FP8 | 8 | Hopper/Ada/Blackwell datacenter | vLLM, TRT-LLM, SGLang |
| MXFP4 | 4 | Blackwell multi-user | TRT-LLM |
| NVFP4 | 4 | Blackwell multi-user | TRT-LLM |

### GGUF  o padrão de CPU/edge

> **【拓展：GGUF 在边缘推理中的地位】**GGUF é o formato padrão de llama.cpp 和 Ollama, que ocupa a maior posição na teoria da CPU/margem. Q4_K_M 和 Q5_K_M é a produção padrão em 4-5 bits para alcançar quase a qualidade de BF16.

GGUF é um formato de arquivo, não um esquema de quantização por si só. Ele agrupa variantes K-quantificadas (Q2_K, Q3_K_M, Q4_K_M, Q5_K_M, Q6_K, Q8_0) em um recipiente. Q4_K_M e Q5_K_M são os padrões de produção  qualidade próxima de BF16 em 4-5 bits. A melhor escolha para CPU ou Edge serve porque llama.cpp é de longe o motor de inferência de CPU mais rápido.

> GGUF é um formato de arquivo, em si não é um esquema quantificado. Ele vai K-quanta 变体打包在一个容器中. Q4_K_M 和 Q5_K_M é a produção em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato de formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato em formato

Penaltia de throughput em vLLM: ~93 tok/s em 7B  o formato não é otimizado para kernels de GPU. Use GGUF quando o objetivo de implantação é CPU/edge. Não de outra forma.

> O modelo de GGUF é usado em uma CPU/margem, caso contrário não é usado.

### GPTQ  multi-LoRA em VLLM

O GPTQ é um algoritmo de quantização pós-treino com um passo de calibração.

> GPTQ é um tipo de algoritmo de quantificação de formação em curso.

A vitória única: o GPTQ-Int4 suporta adaptadores LoRA em vLLM. Se você estiver servindo um modelo base mais 10 a 50 variantes afinadas (cada uma como um LoRA), o GPTQ é o seu caminho.

>                                                                                                                                                                                                                                                               

### AWQ  o GPU padrão do datacenter

> **【中文解读】**AWQ(Activação-consciente Quantização de Peso) é uma escolha de armazenamento de dados do centro de dados de 2026 推理的默认选择──它保护量化过程中约1% 最显著的权重,配合Marlin-AWQ 内核实现 10.9x 加速──在 7B 模型上达到~741 tok/s,是INT4 格式中 Pass@1最高的──除非需要多 LoRA(选择GPTQ) 或Blackwell FP4(选择 NVFP4),否则应应新 GPU 推理项目默认使用 AWQ──

Quantização de peso consciente de ativação. Protege os ~1% mais salientes durante a quantização. Núcleos Marlin-AWQ: 10,9x velocidade versus ingênuo. ~ 741 tok/s em 7B, melhor Pass@1 entre formatos INT4.

> 激活感知权重量化──保护量化过程中约1% 最显著的权重──Marlin-AWQ 内核:比朴素方法快 10.9 倍──7B 模型约 741 tok/s,INT4 格式中 Pass@1 最高──

Escolha AWQ para o novo GPU de serviço, a menos que você precise de multi-LoRA (GPTQ) ou Blackwell FP4 agressivo (NVFP4).

> Novo GPU 推理项目选择 AWQ, excepto que precise de mais LoRA(((((GPTQ) ou ativar o Blackwell FP4((((((NVFP4)。

### FP8  o meio confiável

> **【拓展：FP8 量化的生产应用】**FP8(8-bit 浮点) é a precisão padrão do cenário de 2026 de qualidade inconciliável. HOPPER TENSOR Cores originais aceleração FP8, Blackwell  sucessão de suporte. FP8                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

FP8 é o padrão seguro de 2026 quando a qualidade não é negociável (razão, médico, código-gen).

> 8-bit 浮点──近乎无损──广泛支持──Hopper Tensor Cores 原生加速FP8──Blackwell 继承──当质量不可妥协时(推理、医疗、代码生成),FP8 é a segurança默认选择──内存节省是INT4的一半,但质量风险远低──

### MXFP4 / NVFP4  Blackwell agressivo

Microescalação FP4. Cada bloco de pesos tem seu próprio fator de escala. Agressivo, mas acelerado por hardware em Blackwell Tensor Cores.

> 微缩放 FP4── cada bloco de peso tem seu próprio factor de aceleração── aceleração mas Blackwell Tensor Cores 硬件加速──相比 FP8 每字节减半Phase 17 · 07 中的经济优势──

Cavernas:
- Ainda não há apoio ao LoRA (inicial de 2026).
  No Japão, o governo de Lorraine foi o primeiro a tomar medidas para impedir a criação de um novo governo.
- A queda de qualidade é visível nas cargas de trabalho pesadas.
  Tradução do inglês para tradução do inglês:
- Valida o seu conjunto de avaliações por modelo.
  Tradução do inglês para tradução inglesa:

### A armadilha de calibração

> **【中文解读】**校准数据集陷:AWQ 和 GPTQ 需要校准数据集来决定保护哪些权重. 普遍使用的C4/WikiText 数据集在领域模型 (代码、医疗、法律) 上会导致错误决策. HumanEval Pass@1 可能下降几百分点. 修复方法是领域内数据校准,通常几百样本就够了,发货前在评估集上验证.

> **【拓展：量化对 LLM 能力的影响】**量化对不同能力的影响程度不同:(1) 简单聊天/摘要INT4 几乎无影响;(2) 翻译/写作INT4 轻微退化;(3) 数学/推理INT4 损失 3-5 分(MATH benchmark);(4) 长上下文理解INT4 在 128K+ contexto 上质量显著下降;(5) 代码生成INT4 在 HumanEval 上下降 2-3 分──核心原则:推理密集型任务应使用FP8或BF16,通用聊天可用INT4──

AWQ e GPTQ exigem um conjunto de dados de calibração  tipicamente C4 ou WikiText. Para modelos de domínio (código, médico, legal), calibrar em texto web genérico permite que o algoritmo tome decisões erradas sobre quais pesos proteger. Pass@1 no HumanEval pode cair vários pontos.

> AWQ e GPTQ 需要校准数据集通常是C4或WikiText──对于领域模型(代码、医疗、法律),在通用网络文本上校准会让算法误决策保护哪些权重──HumanEval Pass@1可能下降几百分点──

A solução é calibrar os dados do domínio, centenas de amostras de domínio são suficientes, testar o conjunto de avaliação antes de ser enviado.

> 修复方法: Used in field data校准── Centenas de áreas de amostras geralmente são suficientes──

### A armadilha de cache KV

> **【中文解读】**KV Cache 陷:AWQ vai reduzir o peso de peso para 4 bits, mas KV Cache é independente, manter em FP16/FP8。70B AWQ  modelo  modelo                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

AWQ reduz os pesos para 4 bits. O cache KV é separado e permanece em FP16/FP8. Para um modelo 70B com AWQ:

- Peso: ~ 35 GB (INT4 a partir de 140 GB).
  Chinese:权重:约35GB (desde 140GB de INT4)
- Cachem KV em 128 conteúdo simultâneo × 2k: ~ 20 GB.
  Tradução do inglês: 128并发 × 2K 上下文的 KV 缓存:约20GB──
- Ativações: ~ 5 GB.
  Tradução do inglês:激活:約5GB──
- Total: ~ 60 GB  cabe no H100 80 GB.
  Chinese Translation:总计: cerca de 60GB适合H100 80GB。

Naivamente "Quantizei o meu modelo para 4 GB" esquece os outros 30-50 GB.

> Simplesmente, acho que "meu modelo se quantificou para 4GB" esqueci-me de 30 a 50GB.

Separadamente, a quantização do cache KV (FP8 KV ou INT8 KV) é uma escolha diferente com suas próprias compensações  afeta diretamente a precisão da atenção e não é uma vitória livre.

> Além disso, KV 缓存量化 (FP8 KV ou INT8 KV) é uma escolha independente com diferentes pesos que afeta diretamente a precisão da atenção, não os benefícios gratuitos.

### AWQ INT4 é perigoso para o raciocínio

Cadeia de pensamento, matemática, código-gen com longo contexto  estes sofrem visiblemente de quantização agressiva. AWQ INT4 perde ~ 3-5 pontos em MATH. Para cargas de trabalho pesadas de raciocínio, envia FP8 ou BF16; aceitar o custo de memória.

> Pensamentos, matemática, desenvolvimento e desenvolvimento de código-fonte:

### Guia de escolha 2026

- Serviço de CPU/edge: GGUF Q4_K_M. Feito.
  中文翻译:CPU/边缘服务:GGUF Q4_K_M。
- Serviço de GPU, chat de rotina, sem LoRA.
  Tradução do português:GPU 服务,通用聊天,无 LoRA:AWQ。
- GPU serve, multi-LoRA: GPTQ com Marlin.
  中文翻译:GPU 服务,多 LoRA:GPTQ + Marlin。
- Carga de trabalho de raciocínio: FP8.
  Tradução do português:
- Centro de dados Blackwell, qualidade validada: NVFP4 + FP8 KV.
  Tradução do inglês para inglês: Blackwell 数据中心,已验证质量:NVFP4 + FP8 KV──
- Ambiguos: executar uma avaliação de 1000 amostras em cada formato candidato.
  No entanto, o resultado foi um resultado positivo.

## Use-o com o framework implementado.
```figure
gpu-memory-breakdown
```

## Usá-lo

`code/main.py`Computa a pegada de memória (pesos + KV + ativações) e o throughput relativo nos seis formatos para uma gama de tamanhos de modelos. Mostra onde o cache KV domina, onde a compressão de peso paga e onde FP8 é a escolha segura.

> `code/main.py`計算一系列模型大小在六种格式下内存占用(权重 + KV + 激活) e em relação à吞吐量── mostrar KV 缓存在在哪里占主导、权重压缩在哪里划算、FP8 在哪里是安全选择──

## Envia-o . Produto .

> **【拓展：量化选型决策树】**2026 anos de quantificação de formato seleção de decisão:(1) CPU/边缘部署 → GGUF Q4_K_M;(2) GPU 通用聊天、无 LoRA → AWQ;(3) GPU 多 LoRA → GPTQ + Marlin;(4) 推理密集型任务 → FP8;(5) Blackwell 数据中心、已验证质量 → NVFP4 + FP8 KV;(6) Não está certo → 在候选格式运行1000样本评估;;

Esta lição produz`outputs/skill-quantization-picker.md`. Tendo em conta o hardware, o tamanho do modelo, o tipo de carga de trabalho e a tolerância à qualidade, escolhe um formato e elabora um plano de calibração/validação.

> 本课产 出 `outputs/skill-quantization-picker.md` Fornecer hardware, modelo, tipo de carga de trabalho e tolerância à qualidade, escolher formato e gerar programa de classificação/verificação.

## Exercícios.

1. Corra .`code/main.py`Para um modelo 70B em 128 simultâneos com contexto 2k, calcular o total de HBM para cada formato.
   Tradução: 运行`code/main.py`◊ Para 128 e 2K em 70B, calcular o total de HBM em cada formato.
2. Se você estava errado sobre a tolerância de qualidade, qual é o caminho de recuperação?
   Chinese Translation: Você tem um modelo de código 7B. Escolha um formato e explicação de razão. Se você julgar errado a tolerância à qualidade, qual é o caminho para a recuperação?
3. Calcule o tamanho do conjunto de dados de calibração necessário para calibrar o AWQ para um modelo de domínio médico.
   O modelo de área de medicina de cálculo AWQ 校准所需的数据集大小──为什么更多数据不总是好?
4. Leia o documento do kernel Marlin-AWQ ou as notas de lançamento. Explique em três frases por que AWQ atinge 741 tok/s em 7B enquanto GPTQ bruto atinge ~712.
   Chinese Translation:阅读 Marlin-AWQ 内核论文或发布说明──用三句话解释为什么AWQ在7B上达到741 tok/s而原始GPTQ 约712──
5. Quando faz sentido combinar pesos AWQ com FP8 KV cache vs manter KV em BF16?
   中文翻译:何时将 AWQ 权重与 FP8 KV 缓存组合有意义,何时保持 BF16 KV?

## Termos-chave .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GGUF | "llama.cpp format" | File format bundling K-quant variants; CPU/edge default |
| Q4_K_M | "Q4 K M" | 4-bit K-quant medium; the production GGUF default |
| GPTQ | "gee pee tee q" | Post-train INT4 with calibration; supports LoRA in vLLM |
| AWQ | "a w q" | Activation-aware INT4; Marlin kernels; best Pass@1 at INT4 |
| Marlin kernels | "fast INT4 kernels" | Custom CUDA kernels for INT4 on Hopper; 10x speedup |
| FP8 | "eight-bit float" | Safe precision default on Hopper/Ada/Blackwell |
| MXFP4 / NVFP4 | "microscaling four" | Blackwell 4-bit FP with per-block scale factors |
| Calibration dataset | "cal data" | Input text used to pick quantization parameters; must match domain |
| KV cache quantization | "KV INT8" | Separate choice from weights; affects attention accuracy |

## Mais leitura 延伸阅读

- [VRLA Tech — LLM Quantization 2026](https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/) índices de referência comparativos.
- [Jarvis Labs — vLLM Quantization Complete Guide](https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks) Números de transmissão por formato.
- [PremAI — GGUF vs AWQ vs GPTQ vs bitsandbytes 2026](https://blog.premai.io/llm-quantization-guide-gguf-vs-awq-vs-gptq-vs-bitsandbytes-compared-2026/) Selecção por formato.
- [vLLM docs — Quantization](https://docs.vllm.ai/en/latest/features/quantization/index.html) formatos e bandeiras suportados.
- [AWQ paper (arXiv:2306.00978)](https://arxiv.org/abs/2306.00978) formulação original da AWQ.
- [GPTQ paper (arXiv:2210.17323)](https://arxiv.org/abs/2210.17323) formulação original do GPTQ.
