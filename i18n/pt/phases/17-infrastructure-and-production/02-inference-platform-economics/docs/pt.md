# Inferência Plataforma Economia  Futebol, juntos, basetão, modal, replicação, qualquer escala 推理 经济学

> O mercado de inferência de 2026 não é mais aluguel de tempo de GPU. Ele se divide em silício personalizado (Groq, Cerebras, SambaNova), plataformas de GPU (Baseten, Together, Fireworks, Modal) e mercados de primeira API (Replicate, DeepInfra).$1/hr per GPU on May 1, 2026, and $A avaliação 4B em tokens 10T+/dia indica o modelo de trabalho orientado pelo volume.$300M Series E at $A regra de posicionamento competitivo é simples: Fireworks otimiza a latência, Together otimiza a largura do catálogo, Baseten otimiza o polish empresarial, Modal otimiza o Python-native DX, Replicate otimiza o alcance multimodal, Anyscale otimiza o Python distribuído. Esta lição dá-lhe uma matriz que você pode entregar a um fundador.

> **【中文解读】**Esta secção apresenta a estrutura de custos, modelos de preços e análise econômica da plataforma de avaliação de serviços.
**Type:** Learn
**Languages:** Python (stdlib, toy per-call economics comparator)
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy per-call economics comparator) | **语言:** Python（标准库，每次调用经济性比较器）
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 01（托管 LLM 平台）, Phase 17 · 04（vLLM 服务内部）

> - Não .**【前置】**O curso de formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em formação em uma.
> - Não .**【类比】**推理平台 = "AI 云服务商"──三类:(1) 定制芯片(Groq/Cerebras/SambaNova) = 专用 CPU;(2) GPU 平台(Baseten/Together/Fireworks/Modal) = 通用云;(3) API 市场(Replicate/DeepInfra) = 应用商店──选型口:Fireworks 低延迟、Together 模型多Baseten 企业级、Modal多原生、Replicate模态广、Anyscale 分布式 Python──

## Objetivos de aprendizagem

- Nomear os três segmentos de mercado (sílico personalizado, plataformas GPU, API-first) e mapear cada fornecedor para um segmento.
  Chinese:                                                                                                                                                                                                                                                              
- Explique por que o modelo de preços da API "por token" se comprime para a curva de custo do motor de serviço, não do hardware.
  Tradução do inglês para o inglês: Explain why "by token" API 定价模型 comprimido para a cost curve do motor de serviço e não o custo do hardware.
- Calcule o custo efetivo por pedido em pelo menos três fornecedores e explique quando o valor por minuto (Baseten, Modal) supera o valor por token.
  Chinese: 計算至少三供应商的每次请求有效成本,并解释按分钟 (Baseito, Modal)何时优于按代币 (Baseito, Modal)
- Identificar qual é a plataforma padrão adequada para uma determinada carga de trabalho (desbordamento sem servidor, alta produção constante, variantes ajustadas, multimodal).
  O que é que é um sistema de trabalho?

## O problema é o problema da introdução

Você avaliou as plataformas de hiperescalagem gerenciadas. Você decidiu que precisava de um fornecedor mais estreito e mais rápido. Fireworks para latência, Together para largura, Baseten para um modelo personalizado afinado. Agora você tem seis opções reais e as páginas de preços não se alinham. Fireworks mostra.$/M tokens; Baseten shows $/minute; Modal shows $/second; Replicate shows $Não se pode compará-los cara a cara sem modelar a carga de trabalho.

> Você avaliou a plataforma de gestão, decidiu que precisa de um fornecedor mais especializado, mais rápido, que busque o atraso, juntos, que busque a amplitude, que busque o modelo de auto-definção. Agora, você tem seis opções reais, mas a página de preços não pode comparar diretamente.$/M tokens；Baseten 显示 $/分钟; Modal 显示 $/秒；Replicate 显示 $/预测──不建模工作负载就无法直接比较── não é possível compará-lo diretamente.

Pior ainda, o modelo de negócios por trás de cada página de preços é diferente. Fireworks executa seu próprio motor personalizado (FireAttention) em GPUs compartilhadas; a taxa por token reflete sua curva de utilização. Baseten dá-lhe GPUs dedicadas Truss +; por minuto reflete exclusividade. Modal é verdadeiro Python servidorless  por segundo de faturamento com subsegundo começo frio. A mesma saída (resposta de MLL), três funções de custo diferentes.

> Pior ainda, cada página de fixação tem diferentes modelos comerciais. Fireworks em GPU compartilhada opera em seu próprio motor de desenvolvimento. FireAttention.

Esta lição modela os seis e diz-lhe quando cada um ganha.

> Esta aula tem seis plataformas, diz-te cada um quando vence.

> **【中文解读】**推理平台市场的核心难题是定价模型不统一――按代币 计费(Fireworks/Together) 按分钟计费(Baseten) 按秒计费(Modal) 按预测计费(Replicate)  响应,背后是完全不同的成本函数──不能只看单价,必须根据工作负载特征建模才能做出正确的选择──

> **【拓展：LLM 推理成本构成】**O custo do LLM 推理主要由GPU 租(H100 约 $2-3/hr）、电力（约 $O custo de avaliação é o principal para melhorar a utilização da GPU e o batch de grandes volumes de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de software de

## O conceito central.

> **【中文解读】**推理平台市场分为三大细分:(1) 自研芯片(Groq LPU、Cerebras WSE、SambaNova RDU) 以 5-10x 解码速度取胜但单价更高;(2) GPU 平台(Baseten、Together、Fireworks、Modal) 运行NVIDIA GPU,介于原始 GPU 租和超级级托管服务之间;(3) API 优先市场(Replicate、DeepInfra、OpenRouter) 强调快速手和广度──

> **【拓展：自研推理芯片竞赛】**Groq's LPU(Language Processing Unit) em Llama 70B 上可实现 300+ tokens/s, é GPU 推理的10x──Cerebras' CS-3 晶圆级引擎可达 2000+ tokens/s──但这些芯片的缺点是灵活性低只能运行特定架构的模型──2025-2026年自研推理芯片投资超过50B $──CB Insights),核心注是推理需求将超过 供应──

### Os três segmentos

**Custom silicon**Groq (LPU), Cerebras (WSE), SambaNova (RDU). Tipicamente 5-10 vezes mais rápido que um cluster baseado em GPU no mesmo modelo. Preço por token mais alto (Groq foi ~ $ 0,99 / M em Llama-70B no final de 2025) mas imbatível para casos de uso sensíveis à latência. Groq é a escolha de produção para agentes de voz e tradução em tempo real.

> **自研芯片** Groq(LPU)、Cerebras(WSE)、SambaNova(RDU)。 normalmente comparado ao modelo de GPU 集群解码速度快 5-10 倍──按代币 价格更高(Groq 2025 年末在 Llama-70B 上约 $0.99/M), mas em relação ao uso de atraso sensível não há igual rival──Groq é um agente de produção e um verdadeiro tradução.

**GPU platforms** Baseten, Together, Fireworks, Modal, Anyscale. Execução em NVIDIA (H100, H200, B200 em 2026) ou às vezes AMD. A camada econômica entre "arrendamento de GPU bruto" (RunPod, Lambda) e "serviço gerenciado hipercaler" (Bedrock).

> **GPU 平台** Baseten、Together、Fireworks、Modal、Anyscale──运行在 NVIDIA(2026 anos H100、H200、B200) ou有时是 AMD 上──"original GPU 租"(RunPod、Lambda) e"云托管服务"(Bedrock) entre a economia层──

**API-first marketplaces** Replicar, DeepInfra, OpenRouter, Fal. Catálogo amplo, pagamento por previsão ou pagamento por segundo, enfatizar o tempo para a primeira chamada.

> **API 优先市场** Replicar 、DeepInfra、OpenRouter、Fal。 amplo catálogo, segundo previsão ou segundo pagamento, enfatizando primeira vez de utilização velocidade。

### Fireworks  Plataforma de GPU optimizada para latência

- Motor FireAttention (custom); comercializado como 4 vezes menor latência do que o vLLM em configurações equivalentes.
  O que é o "FireAttention" (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (FireAttention)) (FireAttention) (FireAttention) (FireAttention) (FireAttention)) (FireAttention) (FireAttention) (FireAttention) (FireAttention) (Fire) (Fire) (FireAttention)) (Fire) (Fire) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F) (F)
- Nível de lote em ~50% de taxa sem servidor para cargas de trabalho não interativas.
  Tradução em chinês: nível de lote de aproximadamente 50% da taxa de serviço de serviço, para carga de trabalho não interactivas.
- O modelo de sintonia perfeita serviu à mesma taxa que o modelo base  um diferencial real contra os provedores que cobram um prêmio pelo seu LoRA.
  Tradução em chinês: micro调模型按基础模型费率服务与对LoRA 收取溢价的供应商相比是真正的差异化因素──
- Meados de 2026: aumento da renda de GPU sob demanda de US $ 1 / hora a partir de 1 de maio de 2026.
  Chinese Language Translation:2026: desde 1 de maio de 2019  按量 GPU 租价 $1/小时──大批量价格可协商──
- Sinais financeiros: Valorização de 4 mil milhões de dólares, 10T+ tokens/dia manuseados.
  Tradução do inglês: $4B 估值,每日处理10T+ token──

### Juntos  Otimizado em largura

- 200+ modelos, incluindo lançamentos de código aberto, dentro de dias após a publicação inicial.
  中文翻译:200+ 模型, incluindo edição aberta de up游
- 50-70% mais barato do que Replicar em modelos equivalentes de LLM  o posicionamento "AI Native Cloud" é volume e catálogo.
  Em tradução do inglês, "AI Origins" é um termo usado para designar um modelo de LLM.
- Inferência + ajuste fino + formação numa API.
  Tradução do inglês: 推理 + 微调 + 训练在一个API 中。

### Baseten  empresa-polonês-otimizado

- Estrutura de truss: embalagens de modelo com dependências, segredos, servidor config em um manifesto.
  Truss 框架:模型打包, contendo dependência, chave, serviço em um sistema de configuração.
- A GPU varia de T4 a B200, cobrança por minuto com uma redução razoável de arranque a frio.
  GPU  Rango de T4 até B200── por minuto, há um razoável arrefecimento de início frio──
- SOC 2 Tipo II, pronto para HIPAA.
  O sistema de saúde é um sistema de saúde que é geralmente utilizado para a saúde.
- $5B valuation, January 2026 Series E ($300 milhões de dólares da CapitalG, IVP, NVIDIA).
  Tradução:$5B 估值，2026 年 1 月 E 轮融资（来自 CapitalG、IVP、NVIDIA 的 $300M) ⋅

### Modal  Python nativo-otimizado

- Infraestrutura como código em Python puro. Decorar uma função com `@modal.function(gpu="A100")`e despedaçar com um comando.
  Tradução do inglês:Pure Python's infrastructure即代码──用`@modal.function(gpu="A100")`Função de decoração,一条命令部署。
- Falta de 2 a 4 segundos com pré-aquecimento; < 1s para modelos pequenos.
  Tradução do inglês:                                                                                                                                                                                                                                                            
- $87M Series B at $1.1B Avaliação (2025).
  Tradução do português:$87M，估值 $1.1B(2025)。

### Replicação  largura multimodal

- A plataforma padrão para modelos de imagem, vídeo e áudio.
  Tradução do inglês em japonês: according prediction payment f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f f
- Ecossistema de integração (Zapier, Vercel, plugins CMS).
  O sistema de gestão de dados é um sistema de gestão de dados.
- Menos competitivo em taxas de LLM por token, mas ganha na variedade multimodal.
  LM 按代币 费率竞争力较弱,但在多模态多样性上胜

### Qualquer escala  Ray-native

- Construído em Ray; RayTurbo é o motor de inferência proprietário da Anyscale (competindo com vLLM).
  O RayTurbo é um motor de pensamento especializado em qualquer escala.
- Melhor para cargas de trabalho distribuídas do Python onde o passo de inferência é um nó em um gráfico maior.
  Tradução do inglês para o português: best adaptation to the thinking steps is the largest node in a diagram of a node of a distributed Python 工作负载──
- Gerenciado Ray clusters; estreita integração com Ray AIR e Ray Serve.
  Tradução do inglês:托管 Ray 集群;与 Ray AIR 和 Ray Serve 紧密集成──

### Per-token versus per-minute  quando cada um ganha

Per-token faz sentido quando a carga de trabalho é insensible à latência e explodiu  você só paga pelo que usa. Por minuto faz sentido quando a utilização é alta e previsível  você bate por token uma vez que você está saturando a GPU.

> Quando a carga de trabalho é insensível ao atraso e se torna mais rápida, o custo de token é mais razoável.

Regra rígida: para cargas de trabalho acima de ~ 30% de utilização sustentada de uma GPU dedicada, por minuto (Baseten, Modal) começa a bater por token (Fireworks, Together). abaixo disso, por token ganha porque você evita pagar por ocioso.

> 粗略规则: Para GPUs especiais 持续利用率 exceção de cerca de 30% de trabalho load,按分钟(Baseten、Modal) start优于符号(Fireworks、Together) ∼低于此值时,按符号获胜,因为避免为空付费──

> **【中文解读】**O núcleo da escolha de um modelo de preço é a taxa de utilização. Por token, o custo é adequado para o desenvolvimento e a baixa frequência de um cenário de uso; por minuto, o custo é adequado para um cenário de alta carga contínua. Quando a taxa de utilização da GPU excede cerca de 30% em minutos, a taxa de utilização é geralmente mais barata.

> **【拓展：推理经济学趋势】**O custo de avaliação do modelo de nível 4 do GPT a partir de 2023 foi reduzido em cerca de 90% em 2024-2026$30/M tokens 降到 2025 年的 $3/M tokens── tendências de impulso incluem: modelo quantização(INT8/INT4)、 melhor lote 调度、自研芯片竞争和开源推理引擎(vLLM/SGLang) 的成熟──预计到2027年,同等质量的推理成本将再降低80%──

### O motor personalizado é o verdadeiro fosso .

Cada plataforma acima do vLLM e SGLang reivindica um motor personalizado. FireAttention, RayTurbo, a pilha de inferência de Baseten. Custom-engine afirma que o marketing de sombras  o enquadramento honesto é que vLLM + SGLang representam cerca de 80% da inferência de código aberto de produção, e os diferenciadores na camada da plataforma são DX, atribuição e SLAs.

> Cada plataforma que ultrapassa o VLLM e o SGLang afirma ter um motor de desenvolvimento próprio. FireAttention, RayTurbo, Baseten, .

### Números que você deve lembrar

- Aluguer de GPU de fogos de artifício: Renda de $1/hora a partir de 1o de maio de 2026.
  Chinese: Fireworks GPU 租:自 2026 年 5 月 1 日起价 $1/小时。
- A reclamação de fogos de artifício: 4 vezes menor latência do que a vLLM em configurações equivalentes.
  No entanto, o que não é um bom trabalho é o que não é.
- Juntos: 50-70% mais barato do que o Replicate em LLM.
  Tradução do idioma:L.L.M. 上比 便宜 50-70%。
- Valoração de base: $5B (Series E, Jan 2026, $300M rodada).
  O que é o "baseten"$5B（E 轮，2026 年 1 月，$300M (轮次)
- Valoração do capital: US$ 1,1 bilhão (Série B, 2025).
  中文翻译:Modal 估值: $1.1B(B 轮,2025)。
- Batidas por minuto por token acima de ~ 30% de utilização sustentada.
  Chinese:                                                                                                                                                                                                                                                              

## Use-o com o framework implementado.
```figure
cost-per-token
```

## Usá-lo

`code/main.py`Comparar os seis fornecedores numa carga de trabalho sintética entre modelos de preços.$/day and effective $- M tokens, para encontrar o equilíbrio entre token e minuto.

> `code/main.py`Comparar os modelos de fixação de preços de seis fornecedores em carga de trabalho sintética.$/天和等效 $/M tokens──运行它找到按代币 和按分钟的亏平点──

> **【中文解读】**實踐部分通過模拟工作負荷對比六供應商的定價模型──關鍵输出是每日成本 (concursão)$/day）和等效每百万 token 成本（$/M tokens), ajudá-lo a encontrar o token e o ponto de intervalo.

## Envia-o . Produto .

Esta lição produz`outputs/skill-inference-platform-picker.md`. Tendo em conta o perfil de carga de trabalho, o SLA e o orçamento, escolhe a plataforma de inferência primária e nomeia o segundo.

> 本课产 出 `outputs/skill-inference-platform-picker.md` atribuição de carga de trabalho  SLA 和预算, escolha de plataforma de avaliação e nome de seleção

> **【拓展：推理平台选型决策树】**选型决策路径:(1) 是否需要 < 50ms TTFT? 是 → Groq/Cerebras;(2) 是否需要自托管/合规? 是 → Baseten/Modal;(3) 是否需要最大模型广度? 是 → Together/OpenRouter;(4) 是否需要多媒体模型? 是 → Replicar/Fal;(5) 默认 → Fireworks(延迟优化) or Together(成本优化)

## Exercícios.

1. Corra .`code/main.py`Em que utilização sustentada o Baseten (por minuto) vence o Fireworks (por token) para um modelo 70B em um H100?
   Tradução: 运行`code/main.py`◊ Baseten (→ min) ⇒ What is the continuous utilization rate of a H100 above 70B 模型优于烟火 (→ min) ⋅ Baseten (→ min) ⇒ What is the continuous utilization rate of a H100 above 70B 模型 superior to fireworks (→ min) ⋅ token (→ min) ⋅
2. O seu produto serve para geração de imagens, chat e conversas, escolha plataformas para cada modalidade e nomeia o padrão de gateway que as unifica.
   Chinese Translation: Seu produto fornece imagens geradas, conversas e conversas em voz e letra.
3. Os fogos de artifício aumentam os preços em 1 dólar por hora no seu modelo primário.
   O primeiro é o de um modelo de construção de um arquiteto de ferro.
4. Um cliente regulamentado requer GPUs SOC 2 Tipo II + HIPAA + dedicados. Quais três plataformas são viáveis e qual ganha no FinOps?
   Chinese: 漢字翻译:一個受监管客户需要SOC 2 Type II + HIPAA + 专用 GPU──哪三平台可行,哪个在FinOps上获胜?
5. Comparar custo por 1.000 previsões para Llama 3.1 70B em Fireworks serverless, Together on demand, Baseten dedicado e Replicate API. Qual é o mais barato em 10 previsões por dia?
   Comparar Llama 3.1 70B em Fireworks 无服务器、Together 按量、Baseten 专用和复制 API 上每1000次预测的成本──每天10次预测哪个最便宜?每天10,000次呢?

## Termos-chave .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|----------|
| Custom silicon | "non-GPU chips" | Groq LPU, Cerebras WSE, SambaNova RDU — optimized for decode | 自研推理芯片——Groq LPU、Cerebras WSE 等 |
| FireAttention | "Fireworks engine" | Custom attention kernel; marketed at 4x lower latency than vLLM | Fireworks 自研注意力引擎，号称比 vLLM 快 4x |
| Truss | "Baseten's format" | Model packaging manifest; dependencies + secrets + serving config | Baseten 的模型打包格式，包含依赖、密钥、服务配置 |
| Per-token | "API pricing" | Charge by tokens consumed; pay for no idle | 按 token 计费——只付实际使用量 |
| Per-minute | "dedicated pricing" | Charge by wall-clock GPU time; wins at high utilization | 按分钟计费——高利用率时更划算 |
| Per-prediction | "Replicate pricing" | Charge per model invocation; common for image/video | 按预测次数计费——常见于图像/视频模型 |
| RayTurbo | "Anyscale engine" | Proprietary inference on Ray; competes with vLLM on Ray clusters | Anyscale 基于 Ray 的自研推理引擎 |
| Batch tier | "50% off" | Non-interactive queue at reduced rate; common on Fireworks, OpenAI | 批量推理队列——半价用于非交互任务 |
| Fine-tuned at base rate | "Fireworks LoRA" | Charge LoRA-served requests at base model's rate (differentiator) | 微调模型按基础模型费率计费 |

## Mais leitura 延伸阅读

- [Fireworks Pricing](https://fireworks.ai/pricing)Tarifas por token, nível de lote, aluguel de GPU.
- [Baseten Pricing](https://www.baseten.co/pricing/) taxas por minuto, capacidade comprometida, níveis de empresa.
- [Modal Pricing](https://modal.com/pricing) taxas de GPU por segundo e nível livre.
- [Together AI Pricing](https://www.together.ai/pricing) Catálogo de modelos e taxas por token.
- [Anyscale Pricing](https://www.anyscale.com/pricing) RayTurbo e gerenciou o preço do Ray.
- [Northflank — Fireworks AI Alternatives](https://northflank.com/blog/7-best-fireworks-ai-alternatives-for-inference) avaliação comparativa.
- [Infrabase — AI Inference API Providers 2026](https://infrabase.ai/blog/ai-inference-api-providers-compared) Paisagem de fornecedores.
